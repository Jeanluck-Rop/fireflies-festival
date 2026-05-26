# serializers.py
from rest_framework import serializers
from .models import Parque, ImagenParque

class ImagenParqueSerializer(serializers.ModelSerializer):
    url = serializers.ImageField(source='imagen')
    class Meta:
        model = ImagenParque
        # El campo 'imagen' es el ImageField del modelo
        fields = ['id', 'url'] 

class ParqueSerializer(serializers.ModelSerializer):
    # Traemos la galería de imágenes usando el serializador de arriba
    imagenes = ImagenParqueSerializer(many=True, read_only=True)

    class Meta:
        model = Parque
        fields = [
            'id', 'nombre', 'direccion', 'descripcion', 
            'latitud', 'longitud', 'imagen_mapa', 'imagenes',
            'horario_apertura', 'horario_cierre'
        ]