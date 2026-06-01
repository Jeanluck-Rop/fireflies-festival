# views.py
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.forms import PasswordResetForm
from djoser.views import UserViewSet
from .models import Parque, Usuario, Reservacion, Hospedaje
from .serializers import ParqueSerializer, UserSerializer, AvatarSerializer, ReservacionSerializer

class UserMeView(APIView):
    """ Gestiona los datos del usuario logueado """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserSerializer(
            request.user, 
            data=request.data, 
            partial=True, 
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"detail": "Cuenta eliminada correctamente."}, status=status.HTTP_204_NO_CONTENT)


class UserAvatarView(APIView):
    """ Gestiona únicamente la carga de la imagen de perfil (avatar) """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request):
        serializer = AvatarSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserResetPasswordView(APIView):
    """ Dispara el correo con el link de restablecer contraseña """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"email": ["Este campo es obligatorio."]}, status=status.HTTP_400_BAD_REQUEST)
        
        if Usuario.objects.filter(email=email).exists():
            form = PasswordResetForm({'email': email})
            if form.is_valid():
                form.save(
                    request=request,
                    use_https=request.is_secure(),
                )
        return Response(status=status.HTTP_204_NO_CONTENT)

class ClienteViewSet(UserViewSet):
    def get_queryset(self):
        # Obtain djoser super's queryset
        queryset = super().get_queryset()
        # Filter only clients (exclude staff and superusers)
        return queryset.filter(rol=Usuario.Rol.CLIENTE, is_staff=False, is_superuser=False)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_staff or request.user.is_superuser or request.user.rol == 'ADMIN':
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        elif request.user == instance:
            return super().destroy(request, *args, **kwargs)

        else:
            return Response(
                {"detail": "Unauthorized deletion."},
                status=status.HTTP_403_FORBIDDEN
            )
    
class ReservacionViewSet(viewsets.ModelViewSet):
    serializer_class = ReservacionSerializer

    def get_queryset(self):
        queryset = Reservacion.objects.select_related('parque', 'hospedaje').all()
        usuario_id = self.request.query_params.get('usuario_id', None)
        if usuario_id is not None:
            queryset = queryset.filter(usuario_id=usuario_id)
            
        return queryset
    
    @action(detail=True, methods=['patch'])
    def cancelar(self, request, pk=None):
        reservacion = self.get_object()
        reservacion.estado = Reservacion.Estado.CANCELADA
        reservacion.save()
        
        return Response(
            {"detail": "Reservación cancelada correctamente"}, 
            status=status.HTTP_200_OK
        )
    
class ParqueViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ParqueSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        hoy = date.today()

        # Subquery
        ocupados_hoy = Reservacion.objects.filter(
            fecha_inicio__lte=hoy,
            fecha_fin__gt=hoy,
        ).exclude(
            estado=Reservacion.Estado.CANCELADA
        ).values('hospedaje_id')

        # Filter how many rooms are available today
        filtro_cabanas = Q(
            hospedajes__tipo=Hospedaje.Tipo.CABANA,
            hospedajes__estado=Hospedaje.Estado.DISPONIBLE
        ) & ~Q(hospedajes__id__in=ocupados_hoy)

        filtro_campings = Q(
            hospedajes__tipo=Hospedaje.Tipo.CAMPING,
            hospedajes__estado=Hospedaje.Estado.DISPONIBLE
        ) & ~Q(hospedajes__id__in=ocupados_hoy)

        # Add count of available rooms today to the queryset
        return Parque.objects.annotate(
            cabanas_libres=Count('hospedajes', filter=filtro_cabanas),
            campings_libres=Count('hospedajes', filter=filtro_campings)
        )
    
