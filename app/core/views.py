# views.py
from rest_framework.decorators import action
from datetime import datetime, timedelta, date
from django.db.models import Count, Q, Min, Max
from decimal import Decimal
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from rest_framework import viewsets, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Parque, Usuario, Hospedaje, Reservacion, EmailNotificacion
from .serializers import ParqueSerializer, UserSerializer, AvatarSerializer, HospedajeSerializer, ReservacionSerializer


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

class HospedajeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hospedaje.objects.all()
    serializer_class = HospedajeSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        """ Endpoint: /api/hospedajes/disponibles/ """
        parque_id = request.query_params.get('parque_id')
        tipo = request.query_params.get('tipo')
        personas = request.query_params.get('personas')
        llegada_str = request.query_params.get('llegada')
        salida_str = request.query_params.get('salida')

        if not all([parque_id, tipo, personas, llegada_str, salida_str]):
            return Response({"error": "Faltan parámetros"}, status=status.HTTP_400_BAD_REQUEST)

        personas = int(personas)
        llegada = datetime.strptime(llegada_str, '%Y-%m-%d').date()
        salida = datetime.strptime(salida_str, '%Y-%m-%d').date()

        hospedajes = Hospedaje.objects.filter(
            parque_id=parque_id, tipo=tipo, capacidad__gte=personas, estado='DISPONIBLE'
        )

        reservaciones_solapadas = Reservacion.objects.filter(
            estado__in=['ACTIVA', 'EN_PROCESO'],
            fecha_inicio__lt=salida,
            fecha_fin__gt=llegada
        )
        hospedajes = hospedajes.exclude(reservaciones__in=reservaciones_solapadas)

        serializer = self.get_serializer(hospedajes, many=True)
        return Response(serializer.data)


class ReservacionViewSet(viewsets.ModelViewSet):
    serializer_class = ReservacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'ADMIN':
            return Reservacion.objects.all().order_by('-created_at')
        return Reservacion.objects.filter(usuario=user).order_by('-created_at')

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

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        reservacion = self.get_object()
        reservacion.estado = 'CANCELADA'
        reservacion.save()
        return Response({"status": "Reservación cancelada"})


class ParqueViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Este ViewSet genera automáticamente los endpoints para:
    - Listar todos los parques (GET /api/parques/)
    - Ver un parque específico (GET /api/parques/<id>/)
    """
    queryset = Parque.objects.filter(activo=True)
    serializer_class = ParqueSerializer
    permission_classes = [AllowAny]

class ParqueViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Este ViewSet genera automáticamente los endpoints para:
    - Listar todos los parques (GET /api/parques/)
    - Ver un parque específico (GET /api/parques/<id>/)
    """
    serializer_class = ParqueSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        hoy = date.today()

        # Subquery
        ocupados_hoy = Reservacion.objects.filter(
            fecha_inicio__lte=hoy,
            fecha_fin__gt=hoy,
        ).exclude(
            estado=Reservacion.Estado.CANCELADA
        ).values('hospedaje_id')

        # Filter how many rooms are available today
        filtro_cabanas = Q(
            hospedajes__tipo=Hospedaje.Tipo.CABANA,
            hospedajes__estado=Hospedaje.Estado.DISPONIBLE
        ) & ~Q(hospedajes__id__in=ocupados_hoy)

        filtro_campings = Q(
            hospedajes__tipo=Hospedaje.Tipo.CAMPING,
            hospedajes__estado=Hospedaje.Estado.DISPONIBLE
        ) & ~Q(hospedajes__id__in=ocupados_hoy)

        # Add count of available rooms today to the queryset
        return Parque.objects.filter(activo=True).annotate(
            cabanas_libres=Count('hospedajes', filter=filtro_cabanas),
            campings_libres=Count('hospedajes', filter=filtro_campings),
            precio_minimo=Min('hospedajes__precio_por_noche'),
            precio_maximo=Max('hospedajes__precio_por_noche'),
            capacidad_minima=Min('hospedajes__capacidad'),
            capacidad_maxima=Max('hospedajes__capacidad')
        )