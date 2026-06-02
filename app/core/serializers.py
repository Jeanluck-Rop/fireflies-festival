# serializers.py
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import Parque, ImagenParque, Usuario, Reservacion, Hospedaje, ImagenHospedaje

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id', 'nombre', 'apellidos', 'email', 'genero', 
            'fecha_nacimiento', 'metodo_pago', 'avatar', 
            'rol', 'is_staff', 'is_superuser', 'created_at',
            'parque_asignado'
        ]
        read_only_fields = ['id', 'avatar', 'rol', 'is_staff', 'is_superuser', 'created_at']

    def to_internal_value(self, data):
        mutable_data = data.copy() if hasattr(data, 'copy') else data
        
        for field in ['fecha_nacimiento', 'genero', 'metodo_pago']:
            if field in mutable_data and mutable_data[field] == "":
                mutable_data[field] = None
                
        return super().to_internal_value(mutable_data)

    def validate_nombre(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value

    def validate_apellidos(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Los apellidos no pueden estar vacíos.")
        return value

    def validate_email(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El correo electrónico no puede estar vacío.")
        
        user = self.context['request'].user
        if Usuario.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("Este correo ya se encuentra registrado por otro usuario.")
        return value

class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['avatar']

class ImagenParqueSerializer(serializers.ModelSerializer):
    url = serializers.ImageField(source='imagen')
    class Meta:
        model = ImagenParque
        fields = ['id', 'url']

class ImagenHospedajeSerializer(serializers.ModelSerializer):
    url = serializers.ImageField(source='imagen')
    class Meta:
        model = ImagenHospedaje
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
            'horario_apertura', 'horario_cierre', 'activo'
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
            'created_at',
            'parque_asignado'
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
    
class UsuarioResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'apellidos', 'email']

class ReservacionSerializer(serializers.ModelSerializer):
    parque = ParqueResumenSerializer(read_only=True)
    hospedaje = HospedajeResumenSerializer(read_only=True)
    usuario = UsuarioResumenSerializer(read_only=True)
    monto = serializers.SerializerMethodField()

    class Meta:
        model = Reservacion
        fields = [
            'id', 'estado', 'tipo_visita', 'fecha_inicio',
            'fecha_fin', 'num_personas', 'monto', 'created_at',
            'parque', 'hospedaje', 'usuario'
        ]

    def get_monto(self, obj):
        if obj.tipo_visita == Reservacion.TipoVisita.CABANA:
            return 2500.00
        return 500.00
    
class HospedajeSerializer(serializers.ModelSerializer):
    imagenes = ImagenHospedajeSerializer(many=True, read_only=True)
    precio = serializers.DecimalField(
        source='precio_por_noche', 
        max_digits=10, 
        decimal_places=2, 
    )

    class Meta:
        model = Hospedaje
        fields = [
            'id', 
            'parque',
            'tipo', 
            'categoria', 
            'capacidad', 
            'estado', 
            'num_camas', 
            'num_banos', 
            'tiene_agua', 
            'tiene_luz', 
            'tiene_regadera', 
            'descripcion', 
            'precio',
            'imagenes'
        ]
