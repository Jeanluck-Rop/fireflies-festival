# serializers.py
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import Parque, ImagenParque, Usuario

class ImagenParqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenParque
        fields = ['id', 'imagen'] 

class ParqueSerializer(serializers.ModelSerializer):
    imagenes = ImagenParqueSerializer(many=True, read_only=True)

    class Meta:
        model = Parque
        fields = [
            'id', 'nombre', 'direccion', 'descripcion', 
            'latitud', 'longitud', 'imagen_mapa', 'imagenes'
        ]

class UsuarioCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = Usuario
        fields = ('id', 'email', 'nombre', 'apellidos', 'password')

class UsuarioSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Usuario
        fields = (
            'id', 
            'email', 
            'nombre', 
            'apellidos', 
            'rol', 
            'metodo_pago', 
            'is_staff', 
            'is_superuser',
            'nivel_admin',
            'created_at' 
        )