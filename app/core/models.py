from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator


class UsuarioManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        usuario = self.model(email=email, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("rol", Usuario.Rol.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Un superusuario debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Un superusuario debe tener is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):

    class Rol(models.TextChoices):
        CLIENTE = "CLIENTE", "Cliente"
        ADMIN = "ADMIN", "Administrador"

    username = None
    first_name = None
    last_name = None

    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    rol = models.CharField(max_length=10, choices=Rol.choices, default=Rol.CLIENTE)
    nivel_admin = models.IntegerField(null=True, blank=True)
    metodo_pago = models.CharField(max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre", "apellidos"]

    objects = UsuarioManager()

    class Meta:
        db_table = "usuario"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.nombre} {self.apellidos} <{self.email}>"

    @property
    def es_cliente(self):
        return self.rol == self.Rol.CLIENTE

    @property
    def es_admin(self):
        return self.rol == self.Rol.ADMIN


class Parque(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=300)
    descripcion = models.TextField(null=True, blank=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    horario_apertura = models.TimeField()
    horario_cierre = models.TimeField()
    imagen_mapa = models.CharField(max_length=500, null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "parque"
        verbose_name = "Parque"
        verbose_name_plural = "Parques"

    def __str__(self):
        return self.nombre


class Hospedaje(models.Model):
    class Tipo(models.TextChoices):
        CABANA = "CABANA", "Cabaña"
        CAMPING = "CAMPING", "Camping"

    class Categoria(models.TextChoices):
        INDIVIDUAL = "INDIVIDUAL", "Individual"
        PAREJA = "PAREJA", "Pareja"
        FAMILIAR = "FAMILIAR", "Familiar"

    class Estado(models.TextChoices):
        DISPONIBLE = "DISPONIBLE", "Disponible"
        OCUPADO = "OCUPADO", "Ocupado"
        MANTENIMIENTO = "MANTENIMIENTO", "Mantenimiento"

    parque = models.ForeignKey(
        Parque,
        on_delete=models.CASCADE,
        related_name="hospedajes",
    )
    tipo = models.CharField(max_length=10, choices=Tipo.choices)
    categoria = models.CharField(max_length=12, choices=Categoria.choices)
    capacidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    estado = models.CharField(
        max_length=15, choices=Estado.choices, default=Estado.DISPONIBLE
    )
    num_camas = models.PositiveIntegerField(null=True, blank=True)
    num_banos = models.PositiveIntegerField(null=True, blank=True)
    tiene_agua = models.BooleanField(default=False)
    tiene_luz = models.BooleanField(default=False)
    tiene_regadera = models.BooleanField(default=False)
    pos_x = models.FloatField(null=True, blank=True)
    pos_y = models.FloatField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "hospedaje"
        verbose_name = "Hospedaje"
        verbose_name_plural = "Hospedajes"

    def __str__(self):
        return f"{self.get_tipo_display()} {self.get_categoria_display()} - {self.parque.nombre}"


class Reservacion(models.Model):
    class Estado(models.TextChoices):
        ACTIVA = "ACTIVA", "Activa"
        EN_PROCESO = "EN_PROCESO", "En proceso"
        CANCELADA = "CANCELADA", "Cancelada"
        COMPLETADA = "COMPLETADA", "Completada"

    class TipoVisita(models.TextChoices):
        CABANA = "CABANA", "Cabaña"
        CAMPING = "CAMPING", "Camping"

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="reservaciones",
    )
    parque = models.ForeignKey(
        Parque,
        on_delete=models.PROTECT,
        related_name="reservaciones",
    )
    hospedaje = models.ForeignKey(
        Hospedaje,
        on_delete=models.PROTECT,
        related_name="reservaciones",
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    num_personas = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Precio de la reservación"
    )
    tipo_visita = models.CharField(max_length=10, choices=TipoVisita.choices)
    estado = models.CharField(
        max_length=12, choices=Estado.choices, default=Estado.ACTIVA
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reservacion"
        verbose_name = "Reservación"
        verbose_name_plural = "Reservaciones"

    def __str__(self):
        return f"Reserva #{self.id} de {self.usuario.email}"


class EmailNotificacion(models.Model):
    class Tipo(models.TextChoices):
        BIENVENIDA = "BIENVENIDA", "Bienvenida"
        CONFIRMACION = "CONFIRMACION", "Confirmación"
        CANCELACION = "CANCELACION", "Cancelación"
        CAMBIO_P = "CAMBIO_P", "Cambio de contraseña"
        ASIGNACION_ADMIN = "ASIGNACION_ADMIN", "Asignación admin"

    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        ENVIADO = "ENVIADO", "Enviado"
        ERROR = "ERROR", "Error"

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="notificaciones",
    )
    reservacion = models.ForeignKey(
        Reservacion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notificaciones",
    )
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    estado = models.CharField(
        max_length=10, choices=Estado.choices, default=Estado.PENDIENTE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "email_notificacion"
        verbose_name = "Notificación por email"
        verbose_name_plural = "Notificaciones por email"

    def __str__(self):
        return f"{self.get_tipo_display()} a {self.usuario.email} [{self.estado}]"


class ServicioParque(models.Model):
    parque = models.ForeignKey(
        Parque,
        on_delete=models.CASCADE,
        related_name="servicios",
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    icono = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "servicio_parque"
        verbose_name = "Servicio de parque"
        verbose_name_plural = "Servicios de parque"

    def __str__(self):
        return f"{self.nombre} ({self.parque.nombre})"


class ImagenParque(models.Model):
    parque = models.ForeignKey(
        Parque,
        on_delete=models.CASCADE,
        related_name="imagenes",
    )
    imagen = models.ImageField(upload_to='parques')

    class Meta:
        db_table = "imagen_parque"
        verbose_name = "Imagen de parque"
        verbose_name_plural = "Imágenes de parque"


class ImagenHospedaje(models.Model):
    hospedaje = models.ForeignKey(
        Hospedaje,
        on_delete=models.CASCADE,
        related_name="imagenes",
    )
    imagen = models.ImageField(upload_to='hospedajes')

    class Meta:
        db_table = "imagen_hospedaje"
        verbose_name = "Imagen de hospedaje"
        verbose_name_plural = "Imágenes de hospedaje"
