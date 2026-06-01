# poblar_parques.py
import os
import django
from datetime import time
from decimal import Decimal

# 1. Configurar el entorno de Django antes de importar modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fireflies.settings')
django.setup()

# 2. Importar modelos
from core.models import Parque, Hospedaje, ServicioParque

# 3. Definir los datos masivos
DATOS_PARQUES = [
    {
        "nombre": "Bosque Mágico Nanacamilpa",
        "direccion": "Camino al bosque S/N, San Felipe Hidalgo, Nanacamilpa, Tlaxcala",
        "descripcion": "Un santuario natural inmerso en el bosque de coníferas, famoso por su densa población de luciérnagas Macrolampis palaciosi.",
        "lat": 19.4589, "lon": -98.5342,
        "hospedajes": [
            {"tipo": "CABANA", "categoria": "FAMILIAR", "capacidad": 5, "precio": "1800.00", "camas": 3, "banos": 1, "agua": True, "luz": True, "regadera": True, "desc": "Cabaña de madera con fogata exterior."},
            {"tipo": "CAMPING", "categoria": "PAREJA", "capacidad": 2, "precio": "350.00", "agua": True, "luz": False, "desc": "Espacio de 4x4m cerca de los baños comunes."}
        ],
        "servicios": [("Estacionamiento"), ("Baños compartidos"), ("Guía certificado")]
    },
    {
        "nombre": "Centro Ecoturístico Canto del Bosque",
        "direccion": "Av. Revolución 100, Nanacamilpa, Tlaxcala",
        "descripcion": "Experimenta la magia de la naturaleza en nuestras instalaciones equipadas y senderos seguros.",
        "lat": 19.4650, "lon": -98.5400,
        "hospedajes": [
            {"tipo": "CABANA", "categoria": "PAREJA", "capacidad": 2, "precio": "1200.00", "camas": 1, "banos": 1, "agua": True, "luz": True, "regadera": True, "desc": "Cabaña romántica pequeña, alejada del ruido."},
            {"tipo": "CAMPING", "categoria": "FAMILIAR", "capacidad": 6, "precio": "600.00", "agua": True, "luz": True, "desc": "Zona amplia de camping con asadores cercanos."}
        ],
        "servicios": [("Asadores"), ("Venta de antojitos"), ("Seguridad")]
    },
    {
        "nombre": "Santuario Piedra Canteada",
        "direccion": "Camino Ejidal Piedra Canteada, Tlaxcala",
        "descripcion": "Más de 400 hectáreas de bosque de oyamel para caminar en la oscuridad total.",
        "lat": 19.4720, "lon": -98.5510,
        "hospedajes": [
            {"tipo": "CABANA", "categoria": "INDIVIDUAL", "capacidad": 1, "precio": "900.00", "camas": 1, "banos": 1, "agua": True, "luz": True, "regadera": True, "desc": "Cabaña tipo estudio ideal para fotógrafos o viajeros solitarios."},
            {"tipo": "CAMPING", "categoria": "PAREJA", "capacidad": 2, "precio": "300.00", "agua": False, "luz": False, "desc": "Acampada rústica en el corazón del bosque."}
        ],
        "servicios": [("Mirador"), ("Renta de equipo")]
    },
    {
        "nombre": "Villas del Bosque Santa Clara",
        "direccion": "Ejido San José, Nanacamilpa, Tlaxcala",
        "descripcion": "Complejo premium con todas las comodidades sin perder la conexión con el bosque.",
        "lat": 19.4800, "lon": -98.5200,
        "hospedajes": [
            {"tipo": "CABANA", "categoria": "FAMILIAR", "capacidad": 8, "precio": "3500.00", "camas": 4, "banos": 2, "agua": True, "luz": True, "regadera": True, "desc": "Villa grande con terraza y comedor panorámico."},
            {"tipo": "CAMPING", "categoria": "FAMILIAR", "capacidad": 4, "precio": "800.00", "agua": True, "luz": True, "desc": "Glamping: incluye casa de campaña armada y cobijas."}
        ],
        "servicios": [("Restaurante"), ("Wi-Fi en lobby"), ("Estacionamiento")]
    },
    {
        "nombre": "Rancho San José",
        "direccion": "Carretera Nanacamilpa-Mazapa Km 3",
        "descripcion": "Un rancho tradicional adaptado para recibir a familias durante el festival. Granja interactiva disponible de día.",
        "lat": 19.4500, "lon": -98.5100,
        "hospedajes": [
            # Este parque NO tiene cabañas, solo camping (cumpliendo tu regla de negocio)
            {"tipo": "CAMPING", "categoria": "FAMILIAR", "capacidad": 5, "precio": "450.00", "agua": True, "luz": False, "desc": "Espacios verdes amplios junto a los establos."},
            {"tipo": "CAMPING", "categoria": "INDIVIDUAL", "capacidad": 1, "precio": "150.00", "agua": True, "luz": False, "desc": "Espacio para mochileros."}
        ],
        "servicios": [("Baños compartidos"), ("Granja"), ("Fogata grupal")]
    },
    {
        "nombre": "Parque Ecológico Laguna Azul",
        "direccion": "Desviación a la laguna, San Felipe Hidalgo",
        "descripcion": "El único parque del festival que combina el avistamiento de luciérnagas con un cuerpo de agua natural.",
        "lat": 19.4905, "lon": -98.5600,
        "hospedajes": [
            {"tipo": "CABANA", "categoria": "PAREJA", "capacidad": 2, "precio": "1500.00", "camas": 1, "banos": 1, "agua": True, "luz": True, "regadera": True, "desc": "Cabaña flotante o a la orilla de la laguna."},
            {"tipo": "CAMPING", "categoria": "PAREJA", "capacidad": 2, "precio": "400.00", "agua": True, "luz": False, "desc": "Acampada a 50 metros del agua."}
        ],
        "servicios": [("Paseo en lancha de día"), ("Cafetería")]
    },
    {
        "nombre": "Santuario El Madroño",
        "direccion": "Zona alta de la montaña, Camino maderero",
        "descripcion": "Para los aventureros. Una zona de difícil acceso pero con la mayor concentración de luciérnagas por metro cuadrado.",
        "lat": 19.4400, "lon": -98.5700,
        "hospedajes": [
            {"tipo": "CAMPING", "categoria": "FAMILIAR", "capacidad": 4, "precio": "250.00", "agua": False, "luz": False, "desc": "Acampada 100% extrema. Lleva tus propios suministros."}
        ],
        "servicios": [("Paramédicos"), ("Guía especializado")]
    },
    {
        "nombre": "Centro Turístico Xoletongo",
        "direccion": "Comunidad de Xoletongo, Tlaxcala",
        "descripcion": "Administrado por la comunidad local, ofrece recorridos culturales, mitos y leyendas locales antes del avistamiento.",
        "lat": 19.4550, "lon": -98.5250,
        "hospedajes": [
            {"tipo": "CABANA", "categoria": "FAMILIAR", "capacidad": 6, "precio": "2000.00", "camas": 3, "banos": 2, "agua": True, "luz": True, "regadera": True, "desc": "Cabaña rústica con acabados indígenas locales."},
            {"tipo": "CAMPING", "categoria": "PAREJA", "capacidad": 2, "precio": "300.00", "agua": True, "luz": True, "desc": "Cerca del centro comunitario."}
        ],
        "servicios": [("Tienda de artesanías"), ("Recorrido nocturno")]
    },
    {
        "nombre": "Paraje Las Minas",
        "direccion": "Antiguo camino minero S/N",
        "descripcion": "Un terreno histórico que combina la historia minera de la región con el espectáculo natural de las luciérnagas.",
        "lat": 19.4620, "lon": -98.5800,
        "hospedajes": [
            {"tipo": "CABANA", "categoria": "PAREJA", "capacidad": 2, "precio": "1100.00", "camas": 1, "banos": 1, "agua": True, "luz": True, "regadera": False, "desc": "Cabaña construida en roca. Muy fría pero pintoresca."},
            {"tipo": "CAMPING", "categoria": "FAMILIAR", "capacidad": 4, "precio": "350.00", "agua": True, "luz": False, "desc": "Acampada en las explanadas mineras."}
        ],
        "servicios": [("Zona histórica"), ("Estacionamiento")]
    },
    {
        "nombre": "Valle de las Estrellas",
        "direccion": "Camino al Mirador, Lote 4",
        "descripcion": "Un valle abierto donde las luciérnagas se confunden con las estrellas del cielo despejado.",
        "lat": 19.4850, "lon": -98.5300,
        "hospedajes": [
            {"tipo": "CABANA", "categoria": "FAMILIAR", "capacidad": 10, "precio": "4000.00", "camas": 5, "banos": 3, "agua": True, "luz": True, "regadera": True, "desc": "Mega cabaña para grupos grandes. Cuenta con asador propio."},
            {"tipo": "CAMPING", "categoria": "INDIVIDUAL", "capacidad": 1, "precio": "200.00", "agua": True, "luz": True, "desc": "Acampada libre en el valle."}
        ],
        "servicios": [("Observatorio amateur"), ("Baños compartidos"), ("Tienda de abarrotes")]
    }
]

def poblar_base_de_datos():
    print("🧹 Limpiando parques anteriores...")
    Parque.objects.all().delete()  

    print("🌲 Iniciando la creación de 10 parques...")
    
    for idx, datos in enumerate(DATOS_PARQUES, 1):
        # 1. Crear el Parque
        parque = Parque.objects.create(
            nombre=datos["nombre"],
            direccion=datos["direccion"],
            descripcion=datos["descripcion"],
            latitud=datos["lat"],
            longitud=datos["lon"],
            horario_apertura=time(17, 0), # Estandarizamos 5 PM a 11:30 PM
            horario_cierre=time(23, 30),
        )
        print(f"  [{idx}/10] Creado: {parque.nombre}")

        # 2. Crear sus Hospedajes
        for h in datos["hospedajes"]:
            Hospedaje.objects.create(
                parque=parque,
                tipo=h["tipo"],
                categoria=h["categoria"],
                capacidad=h["capacidad"],
                precio_por_noche=Decimal(h["precio"]),
                num_camas=h.get("camas"),
                num_banos=h.get("banos"),
                tiene_agua=h.get("agua", False),
                tiene_luz=h.get("luz", False),
                tiene_regadera=h.get("regadera", False),
                descripcion=h.get("desc", "")
            )

        # 3. Crear sus Servicios
        for nombre_serv in datos["servicios"]:
            ServicioParque.objects.create(
                parque=parque,
                nombre=nombre_serv
            )

    print("\n✅ ¡Base de datos poblada exitosamente con 10 parques distintos y todas sus relaciones!")

if __name__ == '__main__':
    poblar_base_de_datos()