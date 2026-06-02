import secrets
from datetime import datetime, timedelta, date
from decimal import Decimal

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import transaction
from django.db.models import Count, Q
from django.contrib.auth.hashers import make_password

from rest_framework import viewsets, status, serializers, generics
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from djoser.views import UserViewSet

from .models import Parque, Usuario, Hospedaje, Reservacion, EmailNotificacion, ImagenParque, ImagenHospedaje
from .serializers import (ParqueSerializer, UserSerializer, AvatarSerializer, 
                          HospedajeSerializer, ReservacionSerializer, 
                          ImagenParqueSerializer, ImagenHospedajeSerializer)


class UserMeView(APIView):
    """ Gestiona los datos del usuario logueado """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserSerializer(
            request.user, 
            data=request.data, 
            partial=True, 
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"detail": "Cuenta eliminada correctamente."}, status=status.HTTP_204_NO_CONTENT)


class UserAvatarView(APIView):
    """ Gestiona únicamente la carga de la imagen de perfil (avatar) """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request):
        serializer = AvatarSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClienteViewSet(UserViewSet):
    # This excludes superusers
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(rol=Usuario.Rol.CLIENTE, is_staff=False, is_superuser=False)

        email_param = self.request.query_params.get('email', None)
        if email_param is not None:
            queryset = queryset.filter(email__iexact=email_param)

        return queryset
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_staff or request.user.is_superuser or request.user.rol == 'ADMIN':
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        elif request.user == instance:
            return super().destroy(request, *args, **kwargs)

        else:
            return Response(
                {"detail": "Unauthorized deletion."},
                status=status.HTTP_403_FORBIDDEN
            )
            

class ReservacionViewSet(viewsets.ModelViewSet):
    serializer_class = ReservacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Reservacion.objects.select_related('parque', 'hospedaje').all().order_by('-created_at')
        user = self.request.user
        
        # Si no es admin, solo ve sus propias reservas
        if user.rol != 'ADMIN':
            queryset = queryset.filter(usuario=user)
            
        # Filtro adicional por query param si es necesario
        usuario_id = self.request.query_params.get('usuario_id', None)
        if usuario_id is not None and user.rol == 'ADMIN':
            queryset = queryset.filter(usuario_id=usuario_id)
            
        return queryset

    def perform_create(self, serializer):
        data = self.request.data
        llegada = datetime.strptime(data['fecha_inicio'], '%Y-%m-%d').date()
        salida = datetime.strptime(data['fecha_fin'], '%Y-%m-%d').date()
        
        if llegada.month not in [6, 7, 8] or salida.month not in [6, 7, 8]:
            raise serializers.ValidationError({"fecha_inicio": "El festival solo opera de junio a agosto."})
        
        dias_estancia = (salida - llegada).days
        for i in range(dias_estancia):
            dia_actual = llegada + timedelta(days=i)
            if dia_actual.weekday() == 1:
                raise serializers.ValidationError({"fecha_inicio": "El parque cierra los martes por mantenimiento."})

        hospedaje = Hospedaje.objects.get(id=data['hospedaje'])
        noches = dias_estancia if dias_estancia > 0 else 1
        subtotal = hospedaje.precio_por_noche * noches
        precio_total = subtotal + (subtotal * Decimal('0.05'))

        reservacion = serializer.save(usuario=self.request.user, precio_total=precio_total)

        try:            
            asunto = '¡Tu Reservación está Confirmada! - Festival Luciérnagas 2026'
            mensaje = f"""Hola {self.request.user.nombre},

¡Tu reservación ha quedado completada con éxito!

Detalles de tu viaje:
- Parque: {reservacion.parque.nombre}
- Llegada: {llegada}
- Salida: {salida}
- Tipo: {reservacion.hospedaje.get_tipo_display()}
- Personas: {reservacion.num_personas}
- Total pagado: ${precio_total} MXN

¡Te esperamos para vivir la magia del bosque!
"""
            correo = EmailMessage(
                subject=asunto,
                body=mensaje,
                from_email=settings.EMAIL_HOST_USER,
                to=[self.request.user.email]
            )
            correo.send(fail_silently=False)
            
        except Exception as e:
            print(f"Error al enviar correo: {e}")

    @action(detail=True, methods=['patch', 'post'])
    def cancelar(self, request, pk=None):
        reservacion = self.get_object()
        reservacion.estado = Reservacion.Estado.CANCELADA
        reservacion.save()
        return Response(
            {"detail": "Reservación cancelada correctamente"}, 
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'], url_path='admin')
    def crear_desde_admin(self, request):
        data = request.data
        try:
            with transaction.atomic():
                if 'usuario_id' in data:
                    usuario = Usuario.objects.get(id=data['usuario_id'])
                elif 'nuevo_usuario' in data:
                    nuevo_user_data = data['nuevo_usuario']
                    password_temporal = secrets.token_hex(6)
                    
                    usuario = Usuario.objects.create(
                        email=nuevo_user_data['email'],
                        nombre=nuevo_user_data['nombre'],
                        apellidos=nuevo_user_data['apellidos'],
                        rol=Usuario.Rol.CLIENTE,
                        password=make_password(password_temporal)
                    )
                else:
                    return Response({"detail": "Faltan datos del cliente"}, status=status.HTTP_400_BAD_REQUEST)

                hospedaje = Hospedaje.objects.get(id=data['hospedaje_id'])
                parque = Parque.objects.get(id=data['parque_id'])
                
                d1 = datetime.strptime(data['fecha_inicio'], "%Y-%m-%d").date()
                d2 = datetime.strptime(data['fecha_fin'], "%Y-%m-%d").date()
                noches = (d2 - d1).days
                if noches < 1: 
                    noches = 1
                
                precio_calculado = hospedaje.precio_por_noche * noches 

                nueva_reservacion = Reservacion.objects.create(
                    usuario=usuario,
                    parque=parque,
                    hospedaje=hospedaje,
                    fecha_inicio=data['fecha_inicio'],
                    fecha_fin=data['fecha_fin'],
                    tipo_visita=data['tipo_visita'],
                    num_personas=data['num_personas'],
                    precio_total=precio_calculado,
                    estado=Reservacion.Estado.ACTIVA
                )

                return Response({
                    "detail": "Reservación creada exitosamente",
                    "reservacion_id": nueva_reservacion.id
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ParqueViewSet(viewsets.ModelViewSet):
    serializer_class = ParqueSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        hoy = date.today()

        ocupados_hoy = Reservacion.objects.filter(
            fecha_inicio__lte=hoy,
            fecha_fin__gt=hoy,
        ).exclude(
            estado=Reservacion.Estado.CANCELADA
        ).values('hospedaje_id')

        filtro_cabanas = Q(
            hospedajes__tipo=Hospedaje.Tipo.CABANA,
            hospedajes__estado=Hospedaje.Estado.DISPONIBLE
        ) & ~Q(hospedajes__id__in=ocupados_hoy)

        filtro_campings = Q(
            hospedajes__tipo=Hospedaje.Tipo.CAMPING,
            hospedajes__estado=Hospedaje.Estado.DISPONIBLE
        ) & ~Q(hospedajes__id__in=ocupados_hoy)

        return Parque.objects.filter(activo=True).annotate(
            cabanas_libres=Count('hospedajes', filter=filtro_cabanas),
            campings_libres=Count('hospedajes', filter=filtro_campings)
        )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def mis_parques(self, request):
        user = request.user
        queryset = self.get_queryset() 
        if user.is_staff and not user.is_superuser:
            if user.parque_asignado_id:
                queryset = queryset.filter(id=user.parque_asignado_id)
            else:
                queryset = queryset.none()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=True, 
        methods=['post', 'delete'], 
        parser_classes=[MultiPartParser, FormParser]
    )
    def imagenes(self, request, pk=None):
        parque = self.get_object()
        
        if request.method == 'POST':
            archivos = request.FILES.getlist('imagenes')
            
            if not archivos:
                return Response({"detail": "No se enviaron imágenes."}, status=status.HTTP_400_BAD_REQUEST)
                
            nuevas_imagenes = []
            for archivo in archivos:
                img = ImagenParque.objects.create(parque=parque, imagen=archivo)
                nuevas_imagenes.append(img)
                
            serializer = ImagenParqueSerializer(nuevas_imagenes, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        elif request.method == 'DELETE':
            url_imagen = request.query_params.get('url')
            if not url_imagen:
                return Response({"detail": "Falta la URL de la imagen."}, status=status.HTTP_400_BAD_REQUEST)
            
            from urllib.parse import urlparse
            path = urlparse(url_imagen).path
            if path.startswith(settings.MEDIA_URL):
                path = path[len(settings.MEDIA_URL):]
                
            imagen = ImagenParque.objects.filter(parque=parque, imagen=path).first()
            if imagen:
                imagen.delete()
                return Response({"detail": "Imagen eliminada"}, status=status.HTTP_204_NO_CONTENT)
                
            return Response({"detail": "Imagen no encontrada"}, status=status.HTTP_404_NOT_FOUND)
    

class HospedajeViewSet(viewsets.ModelViewSet):
    queryset = Hospedaje.objects.all()
    serializer_class = HospedajeSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        parque_id = request.query_params.get('parque_id')
        tipo = request.query_params.get('tipo')
        fecha_inicio = request.query_params.get('fecha_inicio') or request.query_params.get('llegada')
        fecha_fin = request.query_params.get('fecha_fin') or request.query_params.get('salida')
        num_personas = request.query_params.get('num_personas') or request.query_params.get('personas', 1)

        if not all([parque_id, tipo, fecha_inicio, fecha_fin]):
            return Response({"error": "Faltan parámetros"}, status=status.HTTP_400_BAD_REQUEST)

        hospedajes_base = Hospedaje.objects.filter(
            parque_id=parque_id,
            tipo=tipo,
            capacidad__gte=int(num_personas),
            estado=Hospedaje.Estado.DISPONIBLE
        )

        ocupados = Reservacion.objects.filter(
            hospedaje__parque_id=parque_id,
            fecha_inicio__lt=fecha_fin,  
            fecha_fin__gt=fecha_inicio   
        ).exclude(
            estado__in=['CANCELADA']
        ).values('hospedaje_id')

        disponibles = hospedajes_base.exclude(id__in=ocupados)

        serializer = self.get_serializer(disponibles, many=True)
        return Response(serializer.data)
    
    @action(
        detail=True,
        methods=['post', 'delete'],
        parser_classes=[MultiPartParser, FormParser]
    )
    def imagenes(self, request, pk=None):
        hospedaje = self.get_object()

        if request.method == 'POST':
            archivos = request.FILES.getlist('imagenes')
            if not archivos:
                return Response({"detail": "No se enviaron imágenes."}, status=400)
            nuevas = []
            for archivo in archivos:
                img = ImagenHospedaje.objects.create(hospedaje=hospedaje, imagen=archivo)
                nuevas.append(img)
            serializer = ImagenHospedajeSerializer(nuevas, many=True, context={'request': request})
            return Response(serializer.data, status=201)

        elif request.method == 'DELETE':
            url_imagen = request.query_params.get('url')
            if not url_imagen:
                return Response({"detail": "Falta la URL de la imagen."}, status=status.HTTP_400_BAD_REQUEST)
            
            from urllib.parse import urlparse
            path = urlparse(url_imagen).path
            if path.startswith(settings.MEDIA_URL):
                path = path[len(settings.MEDIA_URL):]
                
            imagen = ImagenHospedaje.objects.filter(hospedaje=hospedaje, imagen=path).first()
            if imagen:
                imagen.delete()
                return Response({"detail": "Imagen eliminada"}, status=status.HTTP_204_NO_CONTENT)
                
            return Response({"detail": "Imagen no encontrada"}, status=status.HTTP_404_NOT_FOUND)


class StaffViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return Usuario.objects.filter(
            rol=Usuario.Rol.ADMIN, 
            is_staff=True, 
            is_superuser=False
        ).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email', '').strip()

        if Usuario.objects.filter(email__iexact=email).exists():
            return Response(
                {"detail": "Ya existe un usuario registrado con este correo electrónico."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            with transaction.atomic():
                password_temporal = secrets.token_hex(6)
                nuevo_staff = Usuario.objects.create(
                    email=email,
                    nombre=data.get('nombre'),
                    apellidos=data.get('apellidos'),
                    rol=Usuario.Rol.ADMIN,
                    is_staff=True,
                    password=make_password(password_temporal),
                    parque_asignado_id=data.get('parque_asignado')
                )
                return Response({
                    "id": nuevo_staff.id,
                    "nombre": nuevo_staff.nombre,
                    "apellidos": nuevo_staff.apellidos,
                    "email": nuevo_staff.email,
                    "parque_asignado": nuevo_staff.parque_asignado_id,
                    "detail": "Staff creado exitosamente."
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance:
            return Response(
                {"detail": "No puedes eliminar tu propia cuenta de staff."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        instance.delete()
        return Response({"detail": "Cuenta de staff eliminada correctamente."}, status=status.HTTP_200_OK)