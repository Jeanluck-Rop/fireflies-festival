# Festival de las Luciérnagas 2026 🌌🐛
¡Bienvenido al sistema de gestión y reservaciones para el Festival de las Luciérnagas! Este proyecto cuenta con una arquitectura desacoplada utilizando un backend en **Django Rest Framework (DRF)** y un frontend interactivo en **Vue.js (Vite)**, todo completamente contenedorizado con **Docker**.

---

## 🛠️ Requisitos Previos
Antes de iniciar, asegúrate de tener instalado en tu sistema:
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (v20.10 o superior)
* **Docker Compose**

---

## 🚀 Guía de Inicio Rápido (Despliegue del Proyecto)

Sigue estos pasos para poner en marcha la aplicación completa desde la carpeta raíz de tu proyecto:

### 1. Situarse en la carpeta de configuración
Abre tu terminal en el directorio del proyecto y dirígete a la carpeta `config/` donde se encuentran los archivos de Docker:
```bash
cd config
```

### 2. Configurar las Variables de Entorno

El sistema requiere un archivo `.env` para la configuración del backend en el directorio `app/` y uno en el directorio `gui/`. Puedes clonar los archivos de ejemplo ejecutando el siguiente comando desde la ruta raíz del proyecto:

```bash
cp app/.env.example app/.env
```
Si eres un ayudante o la profesora, se te proporcionaron los .env oficiales, para las funcionalidades de envíos de correos, en cuyo caso pegalos en las direcciones antes mencionadas.

#### 🔐 Nota sobre la clave secreta (SECRET_KEY):
El archivo .env requiere que generes una clave secreta nueva y segura para Django, puedes generar una clave aleatoria de alta seguridad ejecutando este comando en tu terminal local: 
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 3. Levantar los Contenedores

Dentro de la carpeta `config/`, ejecuta el siguiente comando para construir las imágenes e iniciar todos los servicios (Base de Datos Postgres, API Django y App Vue):

```bash
docker compose up --build
```

> 💡 **Nota de Automatización:** El entorno está optimizado para que, al levantar el contenedor de la interfaz, se ejecute de forma automática el comando `npm install` para instalar las dependencias de Vue. Asimismo, el backend esperará a que la base de datos esté lista para aplicar las migraciones de Django de manera automática. No necesitas ejecutar instalaciones manuales.

---

## 💾 4. Poblar la Base de Datos (Datos Semilla de Prueba)

Para que puedas evaluar el sistema con información real (parques, cabañas, campings y usuarios de prueba) sin necesidad de capturar todo desde cero, abre **otra terminal**, sitúate en la carpeta `config/` y ejecuta el siguiente comando:

```bash
docker compose exec app python poblar_bd.py
```

*Este script inyectará automáticamente los datos semilla indispensables para el funcionamiento interactivo de la plataforma.*

---

## 🌐 URLs de Acceso Local

Una vez que los contenedores muestren que están listos, abre tu navegador e ingresa a la siguiente dirección:

* **Frontend (Aplicación de Cliente/Admin):** [http://localhost:5173](https://www.google.com/search?q=http://localhost:5173)

### 🔑 Credenciales de Acceso para Pruebas (Creadas por el script de población)

Para probar los distintos roles del sistema, puedes iniciar sesión con las siguientes cuentas precargadas:

* **Cuenta de Administrador:**
* **Correo:** `admin_sistema@luciernagas.com`
* **Contraseña:** `AdminPassword123`


* **Cuenta de Cliente de Prueba:**
* **Correo:** `cliente@luciernagas.com`
* **Contraseña:** `Password123`



---

## 🧪 Execution de la Suite de Pruebas Automatizadas (Tests)

El sistema cuenta con **12 pruebas automatizadas** que cubren tres niveles críticos de calidad: **Pruebas de Unidad (PU)** para reglas de negocio, **Pruebas de Integración (PI)** para la interacción con la base de datos/correos, y **Pruebas de Sistema (PS)** para flujos completos *End-to-End*.

Para correr la suite completa de pruebas dentro del entorno de Docker, ejecuta desde la carpeta `config/`:

```bash
docker compose exec app python3 manage.py test core
```

### ¿Qué ocurre internamente al ejecutar los tests?

1. Django crea una base de datos temporal y aislada para no afectar tus datos reales.
2. Levanta un cliente HTTP simulado (`APITestCase`) que inyecta peticiones simulando al frontend.
3. El módulo de mensajería intercepta los e-mails enviados en un casillero virtual (`mail.outbox`) para corroborar que las notificaciones de bienvenida y de confirmación de reservas se despachen correctamente.
4. Tras validar los 12 casos con éxito (`OK`), la base de datos temporal se destruye automáticamente.

---

## 🧹 Limpieza del Entorno

Si deseas detener los contenedores y limpiar los volúmenes de almacenamiento creados, ejecuta dentro de la carpeta `config/`:

```bash
docker compose down -v
```