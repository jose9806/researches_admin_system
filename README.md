# Researches Admin System

Sistema de administración para la gestión de investigadores, grupos y relaciones, con integración de bases de datos externas y un panel de administración moderno y profesional.

## Estructura del Proyecto

```
researches_admin_system/
├── check_connections.py
├── django-error.log
├── docker-compose.yaml
├── Dockerfile
├── entrypoint.sh
├── manage.py
├── poetry.lock
├── pyproject.toml
├── README.md
├── core/                # Configuración y utilidades principales
├── cvlac/               # App para gestión de investigadores (CVLAC)
├── gruplac/             # App para gestión de grupos (GRUPLAC)
├── integration/         # Integración y relaciones entre investigadores y grupos
├── research_admin/      # Configuración global de Django (settings, urls, wsgi)
├── static/              # Archivos estáticos (CSS, imágenes, JS)
│   └── css/
│       └── custom.css   # Estilos personalizados para el panel admin
├── staticfiles/         # Archivos estáticos recolectados
└── templates/
    └── admin/           # Plantillas personalizadas para el admin
```

## Instalación y Ejecución

### 1. Requisitos previos
- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation)
- Docker (opcional, para despliegue)

### 2. Clonar el repositorio
```bash
git clone <url-del-repo>
cd researches_admin_system
```

### 3. Configuración de variables de entorno

El archivo `.env` contiene las variables necesarias para la conexión a la base de datos y otros servicios. **Debes editar este archivo según el entorno en el que vayas a ejecutar el sistema:**

- **Modo local (sin Docker):**
  - Configura las variables para apuntar al host, usuario y contraseña de tu base de datos local o remota.
- **Modo Docker:**
  - Cambia los valores para que apunten a los servicios definidos en `docker-compose.yaml` (por ejemplo, usa `db` como host si usas el contenedor de base de datos).

> **Importante:** Si vas a conectar con bases de datos externas como CVLAC o GRUPLAC, asegúrate de que las variables de conexión en `.env` correspondan al host, usuario y credenciales correctos para cada entorno.

### 4. Instalar dependencias con Poetry
```bash
poetry install
```

### 5. Activar el entorno virtual de Poetry
```bash
poetry shell
```

### 6. Migrar la base de datos
```bash
python manage.py migrate
```

### 7. Crear un superusuario
```bash
python manage.py createsuperuser
```

### 8. Ejecutar el servidor de desarrollo
```bash
python manage.py runserver
```

Accede a [http://localhost:8000/admin/](http://localhost:8000/admin/) para ingresar al panel de administración.

## Uso de Docker (opcional)

Puedes levantar el entorno completo usando Docker y docker-compose:
```bash
docker-compose up --build
```

Recuerda ajustar el archivo `.env` para que las conexiones de base de datos funcionen correctamente dentro de los contenedores.

## Personalización de Estilos

El sistema utiliza un panel de administración completamente personalizado, inspirado en la paleta de colores de Opera GX, para ofrecer una experiencia visual moderna, profesional y amigable.

- Los estilos están definidos en `static/css/custom.css`.
- Se eliminaron fondos blancos y se mejoró el contraste y la legibilidad.
- Se emplean variables CSS para facilitar la personalización de colores y efectos.
- El diseño es 100% responsive, adaptándose a cualquier dispositivo.
- Las plantillas HTML del admin (`templates/admin/`) fueron adaptadas para aprovechar estos estilos.

Puedes modificar `custom.css` para ajustar la paleta o los componentes visuales según tus necesidades.

## Notas adicionales
- El sistema está preparado para integraciones con bases externas (CVLAC, GRUPLAC).
- El código está modularizado en apps Django para facilitar el mantenimiento y la escalabilidad.

---

Si tienes dudas o necesitas soporte, contacta al equipo de desarrollo.