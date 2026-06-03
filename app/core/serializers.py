from djoser.serializers import UserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import Parque, ImagenParque, Usuario, Hospedaje, Reservacion, ImagenHospedaje, ServicioParque

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id', 'nombre', 'apellidos', 'email', 'genero', 
            'fecha_nacimiento', 'metodo_pago', 'avatar', 
            'rol', 'is_staff', 'is_superuser', 'created_at',
            'parque_asignado', 'nivel_admin'
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
    
    # Traemos la galería de imágenes y servicios
    imagenes = ImagenParqueSerializer(many=True, read_only=True)
    servicios = ServicioParqueSerializer(many=True, read_only=True)
    hasCabin = serializers.SerializerMethodField()

    class Meta:
        model = Parque
        fields = [
            'id', 'nombre', 'direccion', 'descripcion', 
            'latitud', 'longitud', 'imagenes',
            'cabanas_libres', 'campings_libres',
            'horario_apertura', 'horario_cierre', 'activo',
            'hasCabin', 'servicios',
            'precio_minimo', 'precio_maximo',
            'capacidad_minima', 'capacidad_maxima'
        ]

    def get_hasCabin(self, obj):
        return obj.hospedajes.filter(tipo='CABANA').exists()

class UsuarioCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = Usuario
        fields = ('id', 'email', 'nombre', 'apellidos', 'password')

# --- Serializers de Resumen para el Panel de Administrador ---

class ParqueResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parque
        fields = ['id', 'nombre']

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
            'id', 'parque', 'tipo', 'categoria', 'capacidad', 
            'estado', 'num_camas', 'num_banos', 'tiene_agua', 
            'tiene_luz', 'tiene_regadera', 'descripcion', 
            'precio', 'imagenes'
        ]

class ReservacionSerializer(serializers.ModelSerializer):
    # Lectura anidada
    parque = ParqueResumenSerializer(read_only=True)
    hospedaje = HospedajeResumenSerializer(read_only=True)
    usuario = UsuarioResumenSerializer(read_only=True)
    
    # Escritura (para cuando creas la reservación por API mandando solo los IDs)
    parque_id = serializers.PrimaryKeyRelatedField(queryset=Parque.objects.all(), source='parque', write_only=True, required=False)
    hospedaje_id = serializers.PrimaryKeyRelatedField(queryset=Hospedaje.objects.all(), source='hospedaje', write_only=True, required=False)

    class Meta:
        model = Reservacion
        fields = [
            'id', 'parque', 'parque_id', 'hospedaje', 'hospedaje_id', 'usuario',
            'fecha_inicio', 'fecha_fin', 'num_personas', 'tipo_visita', 
            'estado', 'created_at', 'precio_total'
        ]
        read_only_fields = ['id', 'estado', 'created_at', 'precio_total']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get('request')
        
        # Agregamos alias de 'monto' apuntando al precio_total real
        rep['monto'] = rep.get('precio_total')
        
        # Agregamos las URLs de imágenes al hospedaje anidado
        if 'hospedaje' in rep and rep['hospedaje'] and instance.hospedaje:
            imagenes_urls = []
            for img in instance.hospedaje.imagenes.all():
                if img.imagen:
                    url = img.imagen.url
                    if request is not None:
                        url = request.build_absolute_uri(url)
                    imagenes_urls.append(url)
            rep['hospedaje']['imagenes'] = imagenes_urls
            
        return rep