# views.py
import secrets
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.forms import PasswordResetForm
from djoser.views import UserViewSet
from .models import Parque, Usuario, Reservacion, Hospedaje
from .serializers import ParqueSerializer, UserSerializer, AvatarSerializer, ReservacionSerializer, HospedajeSerializer

from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.db.models import Q, Count
from datetime import datetime, date

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
    # This excludes superusers
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(rol=Usuario.Rol.CLIENTE, is_staff=False, is_superuser=False)

        email_param = self.request.query_params.get('email', None)
        if email_param is not None:
            queryset = queryset.filter(email__iexact=email_param)

        return queryset
    
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
    

    @action(detail=False, methods=['post'], url_path='admin')
    def crear_desde_admin(self, request):
        data = request.data
        try:
            with transaction.atomic(): # Atomic operatons
                
                # Creates or gets the user based on the provided data
                if 'usuario_id' in data:
                    usuario = Usuario.objects.get(id=data['usuario_id'])
                elif 'nuevo_usuario' in data:
                    nuevo_user_data = data['nuevo_usuario']
                    # Django crea una contraseña aleatoria segura
                    password_temporal = secrets.token_hex(6)
                    
                    usuario = Usuario.objects.create(
                        email=nuevo_user_data['email'],
                        nombre=nuevo_user_data['nombre'],
                        apellidos=nuevo_user_data['apellidos'],
                        rol=Usuario.Rol.CLIENTE,
                        password=make_password(password_temporal)
                    )
                else:
                    return Response({"detail": "Faltan datos del cliente"}, status=status.HTTP_400_BAD_REQUEST)

                hospedaje = Hospedaje.objects.get(id=data['hospedaje_id'])
                parque = Parque.objects.get(id=data['parque_id'])
                
                d1 = datetime.strptime(data['fecha_inicio'], "%Y-%m-%d").date()
                d2 = datetime.strptime(data['fecha_fin'], "%Y-%m-%d").date()
                noches = (d2 - d1).days
                if noches < 1: 
                    noches = 1
                
                precio_calculado = hospedaje.precio_por_noche * noches 

                # Reservation creation with the calculated price
                nueva_reservacion = Reservacion.objects.create(
                    usuario=usuario,
                    parque=parque,
                    hospedaje=hospedaje,
                    fecha_inicio=data['fecha_inicio'],
                    fecha_fin=data['fecha_fin'],
                    tipo_visita=data['tipo_visita'],
                    num_personas=data['num_personas'],
                    precio_total=precio_calculado,
                    estado=Reservacion.Estado.ACTIVA
                )

                return Response({
                    "detail": "Reservación creada exitosamente",
                    "reservacion_id": nueva_reservacion.id
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
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
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def mis_parques(self, request):
        user = request.user
        hoy = date.today()

        queryset = self.get_queryset() 
        if user.is_staff and not user.is_superuser:
            if user.parque_asignado_id:
                queryset = queryset.filter(id=user.parque_asignado_id)
            else:
                queryset = queryset.none()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class HospedajeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hospedaje.objects.all()
    serializer_class = HospedajeSerializer

    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        parque_id = request.query_params.get('parque_id')
        tipo = request.query_params.get('tipo')
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        num_personas = request.query_params.get('num_personas', 1)

        if not all([parque_id, tipo, fecha_inicio, fecha_fin]):
            return Response([])

        hospedajes_base = Hospedaje.objects.filter(
            parque_id=parque_id,
            tipo=tipo,
            capacidad__gte=num_personas,
            estado=Hospedaje.Estado.DISPONIBLE
        )

        ocupados = Reservacion.objects.filter(
            hospedaje__parque_id=parque_id,
            fecha_inicio__lt=fecha_fin,  # Inicia antes de que termine mi búsqueda
            fecha_fin__gt=fecha_inicio   # Termina después de que inicie mi búsqueda
        ).exclude(
            estado=Reservacion.Estado.CANCELADA
        ).values('hospedaje_id')

        disponibles = hospedajes_base.exclude(id__in=ocupados)

        serializer = self.get_serializer(disponibles, many=True)
        return Response(serializer.data)
    
class StaffViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer # Reutiliza tu UserSerializer existente

    def get_queryset(self):
        return Usuario.objects.filter(
            rol=Usuario.Rol.ADMIN, 
            is_staff=True, 
            is_superuser=False
        ).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email', '').strip()

        if Usuario.objects.filter(email__iexact=email).exists():
            return Response(
                {"detail": "Ya existe un usuario registrado con este correo electrónico."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            with transaction.atomic():
                # Generamos una contraseña aleatoria y segura
                password_temporal = secrets.token_hex(6)
                nuevo_staff = Usuario.objects.create(
                    email=email,
                    nombre=data.get('nombre'),
                    apellidos=data.get('apellidos'),
                    rol=Usuario.Rol.ADMIN,
                    is_staff=True,
                    password=make_password(password_temporal),
                    parque_asignado_id=data.get('parque_asignado') # Puede ser None
                )
                return Response({
                    "id": nuevo_staff.id,
                    "nombre": nuevo_staff.nombre,
                    "apellidos": nuevo_staff.apellidos,
                    "email": nuevo_staff.email,
                    "parque_asignado": nuevo_staff.parque_asignado_id,
                    "detail": "Staff creado exitosamente."
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance:
            return Response(
                {"detail": "No puedes eliminar tu propia cuenta de staff."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        instance.delete()
        return Response({"detail": "Cuenta de staff eliminada correctamente."}, status=status.HTTP_200_OK)