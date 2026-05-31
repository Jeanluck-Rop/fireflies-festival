# serializers.py
from rest_framework import serializers
from .models import Parque, ImagenParque, Usuario

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id', 'nombre', 'apellidos', 'email', 'genero', 
            'fecha_nacimiento', 'metodo_pago', 'avatar', 
            'rol', 'is_staff', 'is_superuser', 'created_at'
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
    class Meta:
        model = ImagenParque
        # El campo 'archivo' es el ImageField de tu modelo
        fields = ['id', 'imagen'] 

class ParqueSerializer(serializers.ModelSerializer):
    # Traemos la galería de imágenes usando el serializador de arriba
    imagenes = ImagenParqueSerializer(many=True, read_only=True)

    class Meta:
        model = Parque
        fields = [
            'id', 'nombre', 'direccion', 'descripcion', 
            'latitud', 'longitud', 'imagen_mapa', 'imagenes'
        ]