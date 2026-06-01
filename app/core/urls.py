# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ParqueViewSet, HospedajeViewSet, ReservacionViewSet


router = DefaultRouter()


router.register(r'parques', ParqueViewSet, basename='parque')
router.register(r'hospedajes', HospedajeViewSet, basename='hospedaje')
router.register(r'reservaciones', ReservacionViewSet, basename='reservacion')


urlpatterns = [
    path('', include(router.urls)),
]