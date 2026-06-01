# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ClienteViewSet, ParqueViewSet, ReservacionViewSet


router = DefaultRouter()


router.register(r'parques', ParqueViewSet, basename='parque')
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'reservaciones', ReservacionViewSet, basename='reservaciones')


urlpatterns = [
    path('', include(router.urls)),
]