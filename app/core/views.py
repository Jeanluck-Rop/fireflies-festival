# views.py
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.forms import PasswordResetForm

from .models import Parque, Usuario
from .serializers import ParqueSerializer, UserSerializer, AvatarSerializer

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

class ParqueViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Este ViewSet genera automáticamente los endpoints para:
    - Listar todos los parques (GET /api/parques/)
    - Ver un parque específico (GET /api/parques/<id>/)
    """
    queryset = Parque.objects.filter(activo=True)
    serializer_class = ParqueSerializer
    permission_classes = [AllowAny]
