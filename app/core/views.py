# views.py
from rest_framework import viewsets
from .models import Parque, Usuario
from rest_framework.permissions import AllowAny
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
