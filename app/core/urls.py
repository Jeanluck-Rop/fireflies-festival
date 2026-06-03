# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ParqueViewSet, 
    HospedajeViewSet, 
    ReservacionViewSet, 
    ClienteViewSet, 
    StaffViewSet
)

router = DefaultRouter()

# Endpoints originales y nuevos unificados
router.register(r'parques', ParqueViewSet, basename='parque')
router.register(r'hospedajes', HospedajeViewSet, basename='hospedaje')
router.register(r'reservaciones', ReservacionViewSet, basename='reservacion')
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'staff', StaffViewSet, basename='staff')

urlpatterns = [
    path('', include(router.urls)),
]