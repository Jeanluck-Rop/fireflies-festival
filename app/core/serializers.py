# serializers.py
from rest_framework import serializers
from .models import Parque, ImagenParque

class ImagenParqueSerializer(serializers.ModelSerializer):
    url = serializers.ImageField(source='imagen')
    class Meta:
        model = ImagenParque
        fields = ['id', 'url'] 

class ParqueSerializer(serializers.ModelSerializer):
    cabanas_libres = serializers.IntegerField(read_only=True)
    campings_libres = serializers.IntegerField(read_only=True)
    imagenes = ImagenParqueSerializer(many=True, read_only=True)

    class Meta:
        model = Parque
        fields = [
            'id', 'nombre', 'direccion', 'descripcion', 
            'latitud', 'longitud', 'imagen_mapa', 'imagenes',
            'cabanas_libres', 'campings_libres',
            'horario_apertura', 'horario_cierre'
        ]