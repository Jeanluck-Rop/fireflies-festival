# serializers.py
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import Parque, ImagenParque, Usuario, Reservacion, Hospedaje

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

# For reservations
class ParqueResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parque
        fields = ['id', 'nombre', 'imagen_mapa']

class HospedajeResumenSerializer(serializers.ModelSerializer):
    nombre = serializers.SerializerMethodField()
    class Meta:
        model = Hospedaje
        fields = ['id', 'nombre']

    def get_nombre(self, obj):
        return f"{obj.get_tipo_display()} {obj.get_categoria_display()}"

class ReservacionSerializer(serializers.ModelSerializer):
    parque = ParqueResumenSerializer(read_only=True)
    hospedaje = HospedajeResumenSerializer(read_only=True)
    
    monto = serializers.SerializerMethodField()

    class Meta:
        model = Reservacion
        fields = [
            'id', 'estado', 'tipo_visita', 'fecha_inicio',
            'fecha_fin', 'num_personas', 'monto', 'created_at',
            'parque', 'hospedaje'
        ]

    def get_monto(self, obj):
        if obj.tipo_visita == Reservacion.TipoVisita.CABANA:
            return 2500.00
        return 500.00