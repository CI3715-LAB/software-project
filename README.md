# SAGTMA

Este proyecto describe la implementación del método de desarrollo de software XP por el equipo CDT para la gestión de un taller mecánico automotriz. Incluye junto con la descripción de este ciclo de vida iterativo e incremental para el proyecto, los artefactos o documentos con los que se gestionan las tareas de adquisición y suministro: requisitos, control y seguimiento del avance, así como las responsabilidades y compromisos de los participantes en el proyecto.

# Componentes del proyecto

El sistema se divide en los siguientes módulos y submódulos:

* Eventos: Registra las acciones que los usuarios ejecutan sobre el sistema.
* Usuarios: Modelos de datos de usuarios que administran el sistema.
  * Roles: Niveles de permisología asociados a los usuarios.
* Proyectos: Proyectos de trabajo del taller que relaciona clientes, vehículos y planes de acción.
  * Planes de acción: Reporte de recursos humanos, materiales y costos asociados a un proyecto.
  * Acciones: Serie de actividades que componen el plan de trabajo.
  * Recursos Humanos: Reporte de recursos humanos y costos.
  * Materiales e Insumos: Reporte de recursos materiales y costos.
* Clientes: Controla la información asociada a los dueños de vehículos que solicitan servicios en el taller automotriz.
* Vehículos: Información detallada de los vehículos de los clientes.
* Materiales: Registro de los materiales necesarios para cumplir con las labores requeridas en los proyectos.
  * Unidades: Unidades de medida asociada a los materiales.
  * Categorías: Categorías que clasifican los tipos de materiales.

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

## Pruebas

El proyecto valida las funcionalidades de cada uno de los módulos y submódulos utilizando 3 aproximaciones de pruebas:

### Pruebas unitarias

Cada módulo realiza pruebas unitarias sobre los casos borde, casos de malicia y casos esperados sobre cada una de las funciones escritas dentro de cada módulo. Estas pruebas utilizan el módulo de python Unittest.

### Pruebas de integración

Realiza purbeas de casos borde, malicia y casos esperados sobre cada uno de los módulos y sobre las interacciónes entre cada uno de ellos. Al igual que el con la pruebas unitarias, se utiliza la librería Unittest.

### Pruebas de interfaces

Para este tipo de pruebas se procura verificar que los flujos en la interfaces de usuario cumplen con lo planificado en el diseño de la interface y la experiencia de usuario.
