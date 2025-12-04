# 🚀 Guía Rápida: Desplegar en Railway

## Paso 1: Subir a GitHub

Si aún no has subido tu código a GitHub:

```bash
# Inicializar git (si no está inicializado)
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Configuración completa para Railway"

# Conectar con tu repositorio de GitHub
git remote add origin https://github.com/TU-USUARIO/sistema-universitario.git

# Subir el código
git push -u origin main
```

## Paso 2: Crear Cuenta en Railway

1. Ve a: https://railway.app
2. Click en **"Login"** o **"Start a New Project"**
3. Selecciona **"Login with GitHub"**
4. Autoriza Railway a acceder a tu cuenta de GitHub

## Paso 3: Crear Nuevo Proyecto

1. En el dashboard de Railway, click en **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Busca y selecciona tu repositorio **`sistema-universitario`**
4. Railway comenzará a desplegar automáticamente

## Paso 4: Esperar el Despliegue

Railway detectará automáticamente:
- ✅ `Procfile` - Comando para iniciar
- ✅ `requirements.txt` - Dependencias Python
- ✅ `runtime.txt` - Python 3.11

El despliegue tomará 2-3 minutos.

## Paso 5: Ver los Logs

Mientras se despliega:
1. Click en tu proyecto
2. Ve a la pestaña **"Deployments"**
3. Click en el deployment activo
4. Verás los logs en tiempo real

Deberías ver:
```
[OK] Conexion establecida con la base de datos
============================================================
  SISTEMA UNIVERSITARIO - GESTIÓN ACADÉMICA
============================================================
```

## Paso 6: Obtener tu URL

1. En el dashboard del proyecto
2. Click en **"Settings"**
3. Busca la sección **"Domains"**
4. Railway te asignará una URL como: `https://sistema-universitario-production-XXXX.up.railway.app`
5. O puedes generar un dominio personalizado

## Paso 7: Inicializar la Base de Datos

**IMPORTANTE:** La primera vez que accedas, necesitas inicializar la base de datos.

### Opción A: Desde Railway Shell (Recomendado)

1. En tu proyecto de Railway
2. Ve a la pestaña de tu servicio
3. Click en los 3 puntos (...) → **"Shell"**
4. Ejecuta estos comandos:

```bash
python database/init_db.py
python database/seed_data.py
```

### Opción B: Desde Build Command

1. Ve a **Settings** → **Build**
2. Agrega en **"Build Command"**:
```bash
python database/init_db.py && python database/seed_data.py
```

## Paso 8: ¡Probar tu Aplicación!

Visita tu URL de Railway y accede con:

**DOCENTE:**
- URL: `tu-url/login/docente`
- Email: `docente@demo.com`
- Password: `docente123`

**ADMINISTRATIVO:**
- URL: `tu-url/login/administrativo`
- Email: `administrativo@demo.com`
- Password: `admin123`

## 🎉 ¡Listo!

Tu aplicación está desplegada en Railway con:
- ✅ Base de datos SQLite persistente
- ✅ Deploy automático con cada push a GitHub
- ✅ HTTPS configurado automáticamente
- ✅ Logs en tiempo real

## Troubleshooting

### Si ves error "ModuleNotFoundError"
Verifica que `requirements.txt` esté correcto y haz un nuevo deploy.

### Si la base de datos está vacía
Ejecuta los comandos de inicialización desde el Shell de Railway.

### Si el servidor no inicia
Revisa los logs en Railway → Deployments → Click en el deployment activo.

---

**¿Necesitas ayuda?** Revisa los logs en Railway para ver cualquier error.
