# serializers.py
from rest_framework import serializers
from .models import Parque, ImagenParque, Usuario, Hospedaje, Reservacion, ImagenHospedaje, ServicioParque

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id', 'nombre', 'apellidos', 'email', 'genero', 
            'fecha_nacimiento', 'metodo_pago', 'avatar', 
            'rol', 'is_staff', 'is_superuser', 'created_at',
            'parque_asignado'
        ]
        read_only_fields = ['id', 'avatar', 'rol', 'is_staff', 'is_superuser', 'created_at', 'parque_asignado']

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

class ReservacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservacion
        fields = [
            'id', 'parque', 'hospedaje', 'fecha_inicio', 'fecha_fin', 
            'num_personas', 'tipo_visita', 'estado', 'created_at', 'precio_total'
        ]
        read_only_fields = ['id', 'estado', 'created_at', 'precio_total']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get('request')
        
        rep['parque'] = {
            'id': instance.parque.id,
            'nombre': instance.parque.nombre,
            'imagen_mapa': instance.parque.imagen_mapa
        }
        
        imagenes_urls = []
        for img in instance.hospedaje.imagenes.all():
            if img.imagen:
                url = img.imagen.url
                if request is not None:
                    url = request.build_absolute_uri(url)
                imagenes_urls.append(url)

        rep['hospedaje'] = {
            'id': instance.hospedaje.id,
            'nombre': f"{instance.hospedaje.get_tipo_display()} {instance.hospedaje.get_categoria_display()}",
            'imagenes': imagenes_urls
        }
        
        rep['monto'] = rep['precio_total']
        return rep

class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['avatar']

class ImagenHospedajeSerializer(serializers.ModelSerializer):
    url = serializers.ImageField(source='imagen')
    class Meta:
        model = ImagenHospedaje
        fields = ['id', 'url']

class HospedajeSerializer(serializers.ModelSerializer):
    imagenes = ImagenHospedajeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Hospedaje
        fields = '__all__'

class ImagenParqueSerializer(serializers.ModelSerializer):
    url = serializers.ImageField(source='imagen')
    class Meta:
        model = ImagenParque
        fields = ['id', 'url'] 

class ServicioParqueSerializer(serializers.ModelSerializer):
    icono = serializers.SerializerMethodField()
    
    class Meta:
        model = ServicioParque
        fields = ['id', 'nombre', 'icono']
        
    def get_icono(self, obj):
        return None

class ParqueSerializer(serializers.ModelSerializer):
    cabanas_libres = serializers.IntegerField(read_only=True)
    campings_libres = serializers.IntegerField(read_only=True)
    
    precio_minimo = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    precio_maximo = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    capacidad_minima = serializers.IntegerField(read_only=True)
    capacidad_maxima = serializers.IntegerField(read_only=True)
    
    # Traemos la galería de imágenes
    imagenes = ImagenParqueSerializer(many=True, read_only=True)
    servicios = ServicioParqueSerializer(many=True, read_only=True)
    hasCabin = serializers.SerializerMethodField()

    class Meta:
        model = Parque
        fields = [
            'id', 'nombre', 'direccion', 'descripcion', 
            'latitud', 'longitud', 'imagen_mapa', 'imagenes',
            'cabanas_libres', 'campings_libres',
            'horario_apertura', 'horario_cierre',
            'hasCabin', 'servicios',
            'precio_minimo', 'precio_maximo',
            'capacidad_minima', 'capacidad_maxima',
            'activo'
        ]

    def get_hasCabin(self, obj):
        return obj.hospedajes.filter(tipo='CABANA').exists()