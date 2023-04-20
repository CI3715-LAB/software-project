# SAGTMA

Este proyecto describe la implementación del método de desarrollo de software XP por el equipo CDT para la gestión de un taller mecánico automotriz. Incluye junto con la descripción de este ciclo de vida iterativo e incremental para el proyecto, los artefactos o documentos con los que se gestionan las tareas de adquisición y suministro: requisitos, control y seguimiento del avance, así como las responsabilidades y compromisos de los participantes en el proyecto.

## Desarrollo

### Flask

Agregar el siguiente contenido:

```
# .env

SECRET_KEY=cdc1db14963d4ba7684fa7fd4b74c417
```

```
# .flaskenv

FLASK_APP=app.py
FLASK_DEBUG=TRUE
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5000
```

**Correr la aplicación**

```bash
$ pip install -r requirements.txt
$ flask run
```

Se recomienda crear un entorno virtual de Python antes de ejecutar los pasos descritos.

### Docker Compose

Eso requiere tener instalado docker y docker compose

**Ejecutar la aplicación**

```
$ docker-compose up --build -d
```

**Detener la aplicación*

```
$ docker-compose down -v
```
