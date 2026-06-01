# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ClienteViewSet, ParqueViewSet 


router = DefaultRouter()


router.register(r'parques', ParqueViewSet, basename='parque')
router.register(r'clientes', ClienteViewSet, basename='cliente')


urlpatterns = [
    path('', include(router.urls)),
]