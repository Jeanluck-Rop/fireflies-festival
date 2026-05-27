# Fireflies Festival - Instrucciones de configuración

**Resumen**: Este README describe los pasos para preparar el entorno de desarrollo del proyecto, incluyendo backend Django, frontend (GUI) y servicios (Docker).

**Requisitos previos**
- **Conda**: Tener `conda` instalado.
- **Python**: Tener Python 3.10+ disponible en el entorno Conda.
- **Node / npm**: Para la carpeta `gui`.
- **Docker & Docker Compose**: Para levantar servicios en `config`.

**Pasos de instalación**

1) **Crear y activar entorno Conda**: crea y activa un entorno llamado `fireflies`.

```bash
conda create -n fireflies python=3.10 -y
conda activate fireflies
```

2) **Instalar dependencias de Python**: desde la raíz del proyecto ejecutar:

```bash
pip install -r requirements.txt
```

3) **Instalar dependencias del frontend (GUI)**: entrar en la carpeta `gui` y ejecutar `npm install`:

```bash
cd gui
npm install
```

4) **Levantar servicios con Docker (en `config`)**: entrar en la carpeta `config` y ejecutar:

```bash
cd config
docker compose up -d
```

5) **Migraciones de Django**: volver a la raíz del proyecto y ejecutar:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

**Archivo .env**
Copiar y pegar el siguiente contenido en `app/.env` (archivo ya incluido en el repositorio):

```dotenv
SECRET_KEY=cZkAWI80eGGlzHJfI-FPT6jcmpPQsAj288dYVHpw82xJtGnm5PcA9IXgHnMjRkREAgU
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=fireflies_db
DB_USER=fireflies_user
DB_PASSWORD=fireflies2026
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST_USER=festivalluciernagas2026@gmail.com
EMAIL_HOST_PASSWORD=abcdefryakdhakwu
```