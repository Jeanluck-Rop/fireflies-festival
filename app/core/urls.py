# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ClienteViewSet, ParqueViewSet, ReservacionViewSet, HospedajeViewSet, StaffViewSet


router = DefaultRouter()


router.register(r'parques', ParqueViewSet, basename='parque')
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'reservaciones', ReservacionViewSet, basename='reservaciones')
router.register(r'hospedajes', HospedajeViewSet, basename='hospedajes')
router.register(r'staff', StaffViewSet, basename='staff')

urlpatterns = [
    path('', include(router.urls)),
]