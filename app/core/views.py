# views.py
from rest_framework import viewsets
from .models import *
from rest_framework.permissions import AllowAny
from .serializers import ParqueSerializer
from datetime import date
from django.db.models import Count, Q

class ParqueViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Este ViewSet genera automáticamente los endpoints para:
    - Listar todos los parques (GET /api/parques/)
    - Ver un parque específico (GET /api/parques/<id>/)
    """
    queryset = Parque.objects.filter(activo=True)
    serializer_class = ParqueSerializer
    permission_classes = [AllowAny]

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
    
