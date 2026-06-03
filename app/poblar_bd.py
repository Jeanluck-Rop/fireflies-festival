# poblar_bd.py
import os
import django
import random
from datetime import date, time, timedelta
from decimal import Decimal

# 1. Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fireflies.settings')
django.setup()

# 2. Importar los modelos
from core.models import (
    Usuario, Parque, Hospedaje, ServicioParque, 
    Reservacion, EmailNotificacion
)
from django.contrib.auth.hashers import make_password

def poblar_base_de_datos():
    print("Iniciando la poblacion de la base de datos...")
    
    # ADVERTENCIA: Este paso elimina los datos actuales para evitar duplicados.
    # Si deseas conservar tus datos actuales, comenta las siguientes lineas.
    # print("Limpiando base de datos existente...")
    # EmailNotificacion.objects.all().delete()
    # Reservacion.objects.all().delete()
    # Hospedaje.objects.all().delete()
    # ServicioParque.objects.all().delete()
    # Parque.objects.all().delete()
    # Usuario.objects.exclude(is_superuser=True).delete() # Mantenemos al superusuario si existe

    # ==========================================
    # POBLAR USUARIOS (22 Registros)
    # ==========================================
    print("Creando usuarios...")
    usuarios_creados = []
    
    # Crear 2 Administradores
    for i in range(1, 3):
        admin = Usuario.objects.create(
            nombre=f"Admin{i}",
            apellidos="Sistema",
            email=f"admin{i}@festival.com",
            password=make_password("password123"),
            rol=Usuario.Rol.ADMIN,
            is_staff=True
        )
        usuarios_creados.append(admin)

    # Crear 20 Clientes
    nombres_base = ["Carlos", "Ana", "Luis", "Maria", "Jorge", "Lucia", "Miguel", "Sofia", "Pedro", "Elena", "Raul", "Laura", "Diego", "Carmen", "Andres", "Marta", "Fernando", "Patricia", "Roberto", "Teresa"]
    apellidos_base = ["Gomez", "Perez", "Rodriguez", "Lopez", "Martinez", "Gonzalez", "Hernandez", "Garcia", "Fernandez", "Ruiz"]

    for i in range(20):
        cliente = Usuario.objects.create(
            nombre=nombres_base[i],
            apellidos=random.choice(apellidos_base),
            email=f"cliente{i+1}@correo.com",
            password=make_password("password123"),
            rol=Usuario.Rol.CLIENTE,
            genero=random.choice([Usuario.Genero.MASCULINO, Usuario.Genero.FEMENINO]),
            fecha_nacimiento=date(random.randint(1980, 2000), random.randint(1, 12), random.randint(1, 28))
        )
        usuarios_creados.append(cliente)

    # ==========================================
    # POBLAR PARQUES (20 Registros)
    # ==========================================
    print("Creando parques...")
    parques_creados = []
    nombres_parques = [
        "Santuario El Rosario", "Bosque Esmeralda", "Parque Ejidal", "Reserva de la Luz",
        "Santuario Santa Clara", "Valle de las Luciernagas", "Parque Nacional La Montaña",
        "EcoParque Los Pinos", "Sendero Brillante", "Bosque Magico", "Reserva Natural El Cedro",
        "Santuario Los Encinos", "Parque Ecologico Oyamel", "Valle Verde", "Cumbres de Luz",
        "Santuario Piedra Herrada", "Bosque Nocturno", "Parque Los Manantiales", 
        "Reserva El Campanario", "Santuario La Mesa"
    ]

    for i, nombre in enumerate(nombres_parques):
        parque = Parque.objects.create(
            nombre=nombre,
            direccion=f"Carretera Principal Km {i+1}, Municipio Central",
            descripcion=f"Un hermoso parque natural dedicado a la conservacion. Ideal para el avistamiento de luciernagas. Este es el parque numero {i+1}.",
            latitud=19.0 + (random.random() * 1.5),  # Coordenadas realistas centro de Mexico
            longitud=-99.0 - (random.random() * 1.5),
            horario_apertura=time(17, 0),
            horario_cierre=time(23, 0),
            activo=True
        )
        parques_creados.append(parque)

    # ==========================================
    # POBLAR SERVICIOS (40 Registros - 2 por parque)
    # ==========================================
    print("Creando servicios de parques...")
    servicios_lista = ["Estacionamiento", "Banos publicos", "Zona de comida", "Guias certificados", "Tienda de recuerdos", "Seguridad 24h", "Asistencia medica"]
    
    for parque in parques_creados:
        servicios_seleccionados = random.sample(servicios_lista, 2)
        for serv in servicios_seleccionados:
            ServicioParque.objects.create(
                parque=parque,
                nombre=serv,
                descripcion=f"Servicio de {serv.lower()} disponible durante toda la visita."
            )

    # ==========================================
    # POBLAR HOSPEDAJES (60 Registros - 3 por parque)
    # ==========================================
    print("Creando hospedajes...")
    hospedajes_creados = []
    
    for parque in parques_creados:
        # 1 Cabana por parque
        cabana = Hospedaje.objects.create(
            parque=parque,
            tipo=Hospedaje.Tipo.CABANA,
            categoria=random.choice([Hospedaje.Categoria.PAREJA, Hospedaje.Categoria.FAMILIAR]),
            capacidad=random.randint(2, 6),
            precio_por_noche=Decimal(random.randint(1000, 3000)),
            estado=Hospedaje.Estado.DISPONIBLE,
            num_camas=random.randint(1, 3),
            num_banos=1,
            tiene_agua=True,
            tiene_luz=True,
            tiene_regadera=True,
            descripcion="Hermosa cabana equipada con todas las comodidades en medio del bosque."
        )
        hospedajes_creados.append(cabana)

        # 2 Zonas de Camping por parque
        for _ in range(2):
            camping = Hospedaje.objects.create(
                parque=parque,
                tipo=Hospedaje.Tipo.CAMPING,
                categoria=random.choice([Hospedaje.Categoria.INDIVIDUAL, Hospedaje.Categoria.PAREJA]),
                capacidad=random.randint(1, 4),
                precio_por_noche=Decimal(random.randint(200, 600)),
                estado=Hospedaje.Estado.DISPONIBLE,
                tiene_agua=random.choice([True, False]),
                tiene_luz=False,
                tiene_regadera=False,
                descripcion="Espacio seguro y delimitado para instalar tu propia casa de campana."
            )
            hospedajes_creados.append(camping)

    # ==========================================
    # POBLAR RESERVACIONES Y CORREOS (20 Registros)
    # ==========================================
    print("Creando reservaciones y notificaciones de correo...")
    clientes = [u for u in usuarios_creados if u.rol == Usuario.Rol.CLIENTE]
    
    for i in range(20):
        cliente = random.choice(clientes)
        hospedaje = random.choice(hospedajes_creados)
        parque = hospedaje.parque
        
        # Generar fechas en la temporada del festival (Junio a Agosto 2026)
        mes = random.randint(6, 8)
        dia_inicio = random.randint(1, 25)
        fecha_llegada = date(2026, mes, dia_inicio)
        
        # Evitar que la reserva caiga en martes (regla de negocio del backend)
        if fecha_llegada.weekday() == 1:
            fecha_llegada += timedelta(days=1)
            
        noches = random.randint(1, 3)
        fecha_salida = fecha_llegada + timedelta(days=noches)
        
        # Calcular precio
        subtotal = hospedaje.precio_por_noche * noches
        precio_total = subtotal + (subtotal * Decimal('0.05')) # Agregamos el 5% de servicio que tienes en views

        reservacion = Reservacion.objects.create(
            usuario=cliente,
            parque=parque,
            hospedaje=hospedaje,
            fecha_inicio=fecha_llegada,
            fecha_fin=fecha_salida,
            num_personas=random.randint(1, hospedaje.capacidad),
            precio_total=precio_total,
            tipo_visita=hospedaje.tipo,
            estado=random.choice([Reservacion.Estado.ACTIVA, Reservacion.Estado.COMPLETADA])
        )

        # Crear su respectiva notificacion de correo simulada
        EmailNotificacion.objects.create(
            usuario=cliente,
            reservacion=reservacion,
            tipo=EmailNotificacion.Tipo.CONFIRMACION,
            estado=EmailNotificacion.Estado.ENVIADO
        )

    print("¡Poblacion de base de datos completada con exito!")
    print(f"- Usuarios: {len(usuarios_creados)}")
    print(f"- Parques: {Parque.objects.count()}")
    print(f"- Servicios: {ServicioParque.objects.count()}")
    print(f"- Hospedajes: {Hospedaje.objects.count()}")
    print(f"- Reservaciones: {Reservacion.objects.count()}")
    print(f"- Notificaciones: {EmailNotificacion.objects.count()}")

if __name__ == '__main__':
    poblar_base_de_datos()