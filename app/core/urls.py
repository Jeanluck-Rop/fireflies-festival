# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ParqueViewSet 


router = DefaultRouter()


router.register(r'parques', ParqueViewSet, basename='parque')


urlpatterns = [
    path('', include(router.urls)),
]