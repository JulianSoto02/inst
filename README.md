# Sistema Universitario - Gestión Académica

Sistema web para la gestión de docentes, materias, horarios y preferencias académicas.

## Características

- **Gestión de Docentes**: CRUD completo de profesores
- **Gestión de Materias**: Administración de asignaturas
- **Asignaciones**: Vinculación de docentes con materias
- **Preferencias**: Gestión de disponibilidad horaria de docentes
- **Notificaciones**: Sistema de alertas y avisos
- **Autenticación**: Sistema seguro con roles (Docente/Administrativo)

## Tecnologías

- **Backend**: Flask (Python 3.x)
- **Base de Datos**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Arquitectura**: Capas + Patrones de Diseño (Singleton, Repository, Service Layer)
- **Principios**: SOLID

## Instalación Local

### Prerrequisitos

- Python 3.8 o superior
- pip

### Pasos

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd sistema-universitario
```

2. Crear entorno virtual:
```bash
python -m venv venv
```

3. Activar entorno virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

5. Iniciar la aplicación:
```bash
python app.py
```

6. Abrir en el navegador:
```
http://127.0.0.1:5000
```

## Credenciales de Acceso

### Docente
- **URL**: http://127.0.0.1:5000/login/docente
- **Email**: docente@demo.com
- **Password**: docente123

### Administrativo
- **URL**: http://127.0.0.1:5000/login/administrativo
- **Email**: administrativo@demo.com
- **Password**: admin123

## Estructura del Proyecto

```
sistema-universitario/
├── app/
│   ├── models/          # Modelos de datos
│   ├── repositories/    # Capa de acceso a datos
│   ├── services/        # Lógica de negocio
│   ├── patterns/        # Patrones de diseño
│   ├── templates/       # Vistas HTML
│   └── static/          # CSS, JS, imágenes
├── database/            # Base de datos SQLite
├── logs/                # Archivos de log
├── app.py               # Aplicación principal
├── requirements.txt     # Dependencias
└── vercel.json          # Configuración Vercel

```

## Despliegue en Railway (Recomendado ⭐)

Railway es la plataforma ideal para este proyecto porque soporta SQLite con persistencia de datos.

### Pasos para Desplegar:

1. **Crear cuenta en Railway**
   - Ve a [railway.app](https://railway.app)
   - Inicia sesión con tu cuenta de GitHub

2. **Crear nuevo proyecto**
   - Click en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Autoriza Railway a acceder a tu GitHub
   - Selecciona tu repositorio `sistema-universitario`

3. **Configuración automática**
   - Railway detectará automáticamente:
     - `Procfile` → Comando para iniciar el servidor
     - `requirements.txt` → Dependencias Python
     - `runtime.txt` → Versión de Python

4. **Inicializar la base de datos**
   - En el dashboard de Railway, ve a tu proyecto
   - Click en "Settings" → "Environment"
   - No necesitas configurar nada más
   - La base de datos SQLite se creará automáticamente en el primer despliegue

5. **Obtener la URL de tu aplicación**
   - Railway te asignará una URL automáticamente
   - Ejemplo: `https://tu-proyecto.up.railway.app`

6. **Acceder a tu aplicación**
   - **Docente:** `tu-url/login/docente`
     - Email: `docente@demo.com`
     - Password: `docente123`

   - **Administrativo:** `tu-url/login/administrativo`
     - Email: `administrativo@demo.com`
     - Password: `admin123`

### Ventajas de Railway:
- ✅ **Base de datos SQLite persistente** (no se pierde entre despliegues)
- ✅ **Gratis** para proyectos pequeños ($5 crédito/mes)
- ✅ **Deploy automático** con cada push a GitHub
- ✅ **Logs en tiempo real** para debugging
- ✅ **Variables de entorno** fáciles de configurar

---

## Despliegue en Vercel (Alternativa)

**⚠️ Limitación:** Vercel NO soporta persistencia de SQLite. Los datos se reinician en cada deploy.

Si aún deseas usar Vercel:

1. Crear cuenta en [Vercel](https://vercel.com)
2. Conectar repositorio de GitHub
3. Vercel desplegará automáticamente

**Nota:** Los cambios en la base de datos NO persisten. Para persistencia, usa Railway o una base de datos externa (PostgreSQL/MySQL)

## Arquitectura

El sistema implementa:
- **Arquitectura en Capas**: Presentación, Controladores, Servicios, Repositorios, Modelos, Datos
- **Patrón MVC**: Model-View-Controller
- **Patrones de Diseño**: Singleton, Repository, Service Layer, Decorator, Factory
- **Principios SOLID**: SRP, OCP, LSP, ISP, DIP

Ver [ARQUITECTURA_Y_PATRONES.md](ARQUITECTURA_Y_PATRONES.md) para más detalles.

## Pruebas

El código está preparado para:
- Pruebas Unitarias (Back/Front)
- Pruebas de Integración
- Pruebas de Sistema
- Pruebas de Aceptación
- Caja Blanca, Caja Negra, Caja Gris
- Pruebas Funcionales y No Funcionales

## Seguridad

- Autenticación con hash de contraseñas (werkzeug)
- Validación de entrada (XSS, SQL Injection)
- Control de acceso basado en roles
- Sesiones seguras con cookies HTTPOnly
- Logging de operaciones críticas

## Licencia

Este proyecto es de código abierto para fines educativos.

## Autor

Sistema de Gestión Universitaria - 2025
# Proyecto desplegado en Railway
