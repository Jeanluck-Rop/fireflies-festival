# views.py
from rest_framework import viewsets
from .models import Parque
from rest_framework.permissions import AllowAny
from .serializers import ParqueSerializer

class ParqueViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Este ViewSet genera automáticamente los endpoints para:
    - Listar todos los parques (GET /api/parques/)
    - Ver un parque específico (GET /api/parques/<id>/)
    """
    queryset = Parque.objects.filter(activo=True)
    serializer_class = ParqueSerializer
    permission_classes = [AllowAny]
