# views.py
from rest_framework import viewsets, status
from .models import Parque, Usuario
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import ParqueSerializer
from djoser.views import UserViewSet

class ParqueViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Este ViewSet genera automáticamente los endpoints para:
    - Listar todos los parques (GET /api/parques/)
    - Ver un parque específico (GET /api/parques/<id>/)
    """
    queryset = Parque.objects.filter(activo=True)
    serializer_class = ParqueSerializer
    permission_classes = [AllowAny]

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
