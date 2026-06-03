from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Usuario, Parque, Hospedaje, Reservacion

class AuthenticationUnitTests(APITestCase):
    """
    NIVEL: Pruebas de Unidad
    Componentes: Módulo de registro de usuario y Autenticación
    """

    def setUp(self):
        # El método setUp se ejecuta ANTES de cada test para preparar datos de prueba
        self.register_url = '/auth/users/'  # Ruta estándar de registro en Djoser
        self.login_url = '/auth/jwt/create/'   # Ruta de login SimpleJWT
        
        # Creamos un usuario base en la base de datos de pruebas para el test de duplicados y login
        self.usuario_existente = Usuario.objects.create_user(
            email='test@luciernagas.com',
            nombre='Juan',
            apellidos='Pérez',
            password='PasswordSeguro123'
        )

    def test_pu_01_validacion_formato_correo_invalido(self):
        """ PU-01 — Validación de formato de correo electrónico """
        data = {
            "email": "usuariosindominio",  # Correo sin '@' ni '.com'
            "nombre": "Carlos",
            "apellidos": "Gómez",
            "password": "Password123!"
        }
        
        response = self.client.post(self.register_url, data, format='json')
        
        # Esperamos un código 400 (Bad Request) porque el formato está mal
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Verificamos que el error apunte específicamente al campo email
        self.assertIn('email', response.data)

    def test_pu_02_verificacion_correo_duplicado(self):
        """ PU-02 — Verificación de correo duplicado """
        data = {
            "email": "test@luciernagas.com",  # Este correo ya lo creó el setUp arriba
            "nombre": "Juan Copia",
            "apellidos": "Pérez",
            "password": "OtraContrasena123"
        }
        
        response = self.client.post(self.register_url, data, format='json')
        
        # Debe rechazarlo con un 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # El mensaje de error debe indicar que el correo ya está en uso
        self.assertIn('email', response.data)

    def test_pu_03_validacion_credenciales_incorrectas(self):
        """ PU-03 — Validación de credenciales de inicio de sesión """
        data = {
            "email": "test@luciernagas.com",
            "password": "ContrasenaEquivocada"  # No es la del setUp
        }
        
        response = self.client.post(self.login_url, data, format='json')
        
        # Al fallar el login, el sistema debe responder con 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Verificamos que devuelva un mensaje de error genérico de la librería sin detallar qué falló
        self.assertIn('detail', response.data)

class ReservationUnitTests(APITestCase):
    """
    NIVEL: Pruebas de Unidad
    Componente: Servicio de validación de reservaciones (Reglas del Negocio)
    """

    def setUp(self):
        self.reservaciones_url = '/api/reservaciones/'
        
        # Creamos un usuario y lo autenticamos en el cliente de pruebas
        self.usuario = Usuario.objects.create_user(
            email='cliente@luciernagas.com',
            nombre='Maria',
            apellidos='Lopez',
            password='Password123'
        )
        self.client.force_authenticate(user=self.usuario)
        
        self.parque = Parque.objects.create(
            nombre="Bosque de Prueba",
            direccion="Km 10",
            descripcion="Un parque hermoso",
            latitud=19.4,
            longitud=-98.5,
            horario_apertura="08:00:00",
            horario_cierre="18:00:00",
            activo=True
        )
        
        self.hospedaje = Hospedaje.objects.create(
            parque=self.parque,
            tipo="CABANA",
            categoria="ESTANDAR",
            capacidad=4,
            precio_por_noche=1500.00,
            estado="DISPONIBLE"
        )

    def test_pu_04_validacion_fechas_periodo_festival(self):
        """ PU-04 — Validación de fechas de reservación (período del festival de junio a agosto) """
        data = {
            "parque": self.parque.id,
            "hospedaje": self.hospedaje.id,
            "fecha_inicio": "2026-05-15",
            "fecha_fin": "2026-05-18",
            "num_personas": 2,
            "tipo_visita": "CABANA"
        }
        
        response = self.client.post(self.reservaciones_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('fecha_inicio', response.data)
        self.assertEqual(response.data['fecha_inicio'], "El festival solo opera de junio a agosto.")

    def test_pu_05_validacion_dia_martes_en_reservacion(self):
        """ PU-05 — Validación de día martes en reservación (mantenimiento) """
        data = {
            "parque": self.parque.id,
            "hospedaje": self.hospedaje.id,
            "fecha_inicio": "2026-06-08", 
            "fecha_fin": "2026-06-11",     
            "num_personas": 2,
            "tipo_visita": "CABANA"
        }
        
        response = self.client.post(self.reservaciones_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('fecha_inicio', response.data)
        self.assertEqual(response.data['fecha_inicio'], "El parque cierra los martes por mantenimiento.")

class IntegrationTests(APITestCase):
    """
    NIVEL: Pruebas de Integración
    Verifica la interacción entre múltiples componentes (Base de datos, Vistas, Correos).
    """

    def setUp(self):
        self.register_url = '/auth/users/'
        self.login_url = '/auth/jwt/create/'
        self.reservaciones_url = '/api/reservaciones/'

        # Datos base indispensables para reservaciones
        self.parque = Parque.objects.create(
            nombre="Santuario El Rosario",
            direccion="Michoacán",
            descripcion="Zona de luciérnagas",
            latitud=19.6,
            longitud=-100.2,
            horario_apertura="08:00:00",
            horario_cierre="18:00:00",
            activo=True
        )
        self.hospedaje = Hospedaje.objects.create(
            parque=self.parque,
            tipo="CAMPING",
            categoria="ESTANDAR",
            capacidad=2,
            precio_por_noche=500.00,
            estado="DISPONIBLE"
        )

    def test_pi_01_registro_de_usuario_e_inicio_de_sesion(self):
        """ PI-01 — Registro de usuario e inicio de sesión """
        # 1. Flujo de Registro
        registro_data = {
            "email": "nuevo_cliente@luciernagas.com",
            "nombre": "Carlos",
            "apellidos": "Mendoza",
            "password": "PasswordSeguro123"
        }
        response_reg = self.client.post(self.register_url, registro_data, format='json')
        self.assertEqual(response_reg.status_code, status.HTTP_201_CREATED)

        # 2. Flujo de Autenticación inmediata con las mismas credenciales
        login_data = {
            "email": "nuevo_cliente@luciernagas.com",
            "password": "PasswordSeguro123"
        }
        response_log = self.client.post(self.login_url, login_data, format='json')
        
        # Debe otorgar el acceso (200 OK) y devolver un Token JWT válido
        self.assertEqual(response_log.status_code, status.HTTP_200_OK)
        self.assertIn('access', response_log.data)

    def test_pi_02_creacion_de_reservacion_y_estado_activo(self):
        """ PI-02 — Creación de reservación exitosa """
        usuario = Usuario.objects.create_user(
            email='inter@luciernagas.com', nombre='Ana', apellidos='Soto', password='Pass'
        )
        self.client.force_authenticate(user=usuario)

        data = {
            "parque": self.parque.id,
            "hospedaje": self.hospedaje.id,
            "fecha_inicio": "2026-06-19",
            "fecha_fin": "2026-06-22",
            "num_personas": 2,
            "tipo_visita": "CAMPING"
        }
        response = self.client.post(self.reservaciones_url, data, format='json')
        
        if response.status_code != 201:
            print("ERROR EN PI_02:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['estado'], 'ACTIVA')

    def test_pi_03_confirmacion_de_reservacion_y_envio_de_correo(self):
        """ PI-03 — Confirmación de reservación y envío de correo """
        from django.core import mail

        usuario = Usuario.objects.create_user(
            email='correo_test@luciernagas.com', nombre='Luis', apellidos='G', password='Pass'
        )
        self.client.force_authenticate(user=usuario)

        data = {
            "parque": self.parque.id,
            "hospedaje": self.hospedaje.id,
            "fecha_inicio": "2026-07-01",
            "fecha_fin": "2026-07-04",
            "num_personas": 1,
            "tipo_visita": "CAMPING"
        }
        response = self.client.post(self.reservaciones_url, data, format='json')
        
        if response.status_code != 201:
            print("ERROR EN PI_03:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, '¡Tu Reservación está Confirmada! - Festival Luciérnagas 2026')
        self.assertIn('Luis', mail.outbox[0].body)

    def test_pi_04_cancelacion_de_reservacion_y_cambio_de_estado(self):
        """ PI-04 — Cancelación de reservación """
        usuario = Usuario.objects.create_user(
            email='cancel@luciernagas.com', nombre='Pedro', apellidos='M', password='Pass'
        )
        self.client.force_authenticate(user=usuario)

        # Creamos una reservación previa de forma directa para poder cancelarla
        reservacion = Reservacion.objects.create(
            usuario=usuario,
            parque=self.parque,
            hospedaje=self.hospedaje,
            fecha_inicio="2026-06-20",
            fecha_fin="2026-06-23",
            num_personas=2,
            tipo_visita="CAMPING",
            precio_total=1500.00,
            estado="ACTIVA"
        )

        # Ejecutamos la acción personalizada @action
        cancel_url = f"{self.reservaciones_url}{reservacion.id}/cancelar/"
        response = self.client.post(cancel_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Volvemos a consultar el objeto desde la base de datos para verificar su actualización real
        reservacion.refresh_from_db()
        self.assertEqual(reservacion.estado, 'CANCELADA')

class SystemTests(APITestCase):
    """
    NIVEL: Pruebas de Sistema (End-to-End)
    Valida flujos completos de extremo a extremo simulando el comportamiento del usuario.
    """

    def setUp(self):
        self.register_url = '/auth/users/'
        self.login_url = '/auth/jwt/create/'
        self.parques_url = '/api/parques/'
        self.reservaciones_url = '/api/reservaciones/'

        # Creamos la infraestructura base en el sistema
        self.parque = Parque.objects.create(
            nombre="Parque Nacional El Chico",
            direccion="Hidalgo",
            descripcion="Bosque de oyamel",
            latitud=20.2,
            longitud=-98.7,
            horario_apertura="07:00:00",
            horario_cierre="17:00:00",
            activo=True
        )
        self.hospedaje = Hospedaje.objects.create(
            parque=self.parque,
            tipo="CABANA",
            categoria="PREMIUM",
            capacidad=5,
            precio_por_noche=2500.00,
            estado="DISPONIBLE"
        )
        
        # Creamos una cuenta de administrador para el flujo PS-03
        self.admin_user = Usuario.objects.create_superuser(
            email='admin_sistema@luciernagas.com',
            nombre='Super',
            apellidos='Admin',
            password='AdminPassword123'
        )

    def test_ps_01_flujo_completo_reservacion_de_cliente(self):
        """ PS-01 — Flujo completo de reservación de cliente """
        from django.core import mail

        # 1. El cliente se registra
        reg_data = {
            "email": "cliente_e2e@luciernagas.com",
            "nombre": "Roberto",
            "apellidos": "Galván",
            "password": "PasswordE2E123"
        }
        res_reg = self.client.post(self.register_url, reg_data, format='json')
        self.assertEqual(res_reg.status_code, status.HTTP_201_CREATED)

        # 2. El cliente inicia sesión
        login_data = {"email": "cliente_e2e@luciernagas.com", "password": "PasswordE2E123"}
        res_log = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(res_log.status_code, status.HTTP_200_OK)
        token = res_log.data['access']

        # Autenticamos el cliente con el token obtenido para los siguientes pasos
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # 3. El cliente consulta la lista de parques (el mapa público)
        res_parques = self.client.get(self.parques_url)
        self.assertEqual(res_parques.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res_parques.data) > 0)

        # 4. El cliente selecciona el parque y completa el formulario de reservación
        res_data = {
            "parque": self.parque.id,
            "hospedaje": self.hospedaje.id,
            "fecha_inicio": "2026-07-10", # Viernes 10 de Julio 2026 (No es martes)
            "fecha_fin": "2026-07-13",    # Lunes 13 de Julio 2026
            "num_personas": 3,
            "tipo_visita": "CABANA"
        }
        res_reserva = self.client.post(self.reservaciones_url, res_data, format='json')
        self.assertEqual(res_reserva.status_code, status.HTTP_201_CREATED)

        # 5. El sistema responde: aparece en "Mis reservaciones" y se envía el correo
        res_mis_reservas = self.client.get(self.reservaciones_url)
        self.assertEqual(res_mis_reservas.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_mis_reservas.data), 1)
        self.assertEqual(len(mail.outbox), 2)

    def test_ps_02_flujo_completo_cancelacion(self):
        """ PS-02 — Flujo completo de cancelación """
        # Creamos un usuario, lo autenticamos y le generamos una reservación activa
        usuario = Usuario.objects.create_user(
            email='cancel_e2e@luciernagas.com', nombre='Luis', apellidos='P', password='Pass'
        )
        self.client.force_authenticate(user=usuario)
        
        reserva = Reservacion.objects.create(
            usuario=usuario, parque=self.parque, hospedaje=self.hospedaje,
            fecha_inicio="2026-08-14", fecha_fin="2026-08-17", num_personas=2,
            tipo_visita="CABANA", precio_total=7500.00, estado="ACTIVA"
        )

        # 1. El cliente accede a sus reservaciones
        res_lista = self.client.get(self.reservaciones_url)
        self.assertEqual(len(res_lista.data), 1)

        # 2. Selecciona la reservación activa y confirma la cancelación
        cancel_url = f"{self.reservaciones_url}{reserva.id}/cancelar/"
        response = self.client.post(cancel_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 3. El estado cambia y la lista se actualiza
        reserva.refresh_from_db()
        self.assertEqual(reserva.estado, 'CANCELADA')

    def test_ps_03_gestion_de_parques_por_administrador(self):
        """ PS-03 — Gestión de parques por administrador """
        # Autenticamos al administrador del sistema
        self.client.force_authenticate(user=self.admin_user)

        # 1. El administrador crea un nuevo parque
        nuevo_parque_data = {
            "nombre": "Bosque Esmeralda",
            "direccion": "EdoMex",
            "descripcion": "Santuario ecoturístico",
            "latitud": 19.1,
            "longitud": -98.8,
            "horario_apertura": "06:00:00",
            "horario_cierre": "16:00:00",
            "activo": True
        }
        response_create = self.client.post(self.parques_url, nuevo_parque_data, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        parque_id = response_create.data['id']

        # 2. El administrador edita el parque existente
        update_data = {"nombre": "Bosque Esmeralda Modificado"}
        response_patch = self.client.patch(f"{self.parques_url}{parque_id}/", update_data, format='json')
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        self.assertEqual(response_patch.data['nombre'], "Bosque Esmeralda Modificado")

        # 3. El administrador consulta todas las reservaciones del sistema
        response_reservas = self.client.get(self.reservaciones_url)
        self.assertEqual(response_reservas.status_code, status.HTTP_200_OK)