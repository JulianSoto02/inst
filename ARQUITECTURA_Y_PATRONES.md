# ARQUITECTURA Y PATRONES DE DISEÑO - SISTEMA UNIVERSITARIO

## 1. ARQUITECTURA DEL SOFTWARE

### 1.1 Arquitectura en Capas (Layered Architecture)

El sistema está organizado en una arquitectura de capas bien definida que separa las responsabilidades:

```
┌─────────────────────────────────────────────────────┐
│                CAPA DE PRESENTACIÓN                 │
│              (Templates HTML + Flask)               │
│   - app/templates/auth/                             │
│   - app/templates/docente/                          │
│   - app/templates/administrativo/                   │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│              CAPA DE CONTROLADORES                  │
│                   (app.py)                          │
│   - Rutas Flask (@app.route)                        │
│   - Decoradores de autenticación                    │
│   - Validación de entrada                           │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│              CAPA DE SERVICIOS                      │
│             (app/services/)                         │
│   - auth_service.py                                 │
│   - docente_service.py                              │
│   - administrativo_service.py                       │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│            CAPA DE REPOSITORIOS                     │
│           (app/repositories/)                       │
│   - usuario_repository.py                           │
│   - materia_repository.py                           │
│   - preferencia_repository.py                       │
│   - notificacion_repository.py                      │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│              CAPA DE MODELOS                        │
│              (app/models/)                          │
│   - usuario.py (Docente, Administrativo)            │
│   - materia.py                                      │
│   - preferencia.py                                  │
│   - notificacion.py                                 │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│           CAPA DE ACCESO A DATOS                    │
│           (app/patterns/singleton.py)               │
│   - DatabaseConnection (Singleton)                  │
│   - Gestión de conexiones SQLite                    │
└─────────────────────────────────────────────────────┘
```

#### Descripción de cada capa:

**1. Capa de Presentación:**
- Archivos: `app/templates/**/*.html`
- Responsabilidad: Renderizar la interfaz de usuario
- Tecnologías: HTML, CSS (styles.css), JavaScript
- Comunicación: Recibe datos del controlador y muestra al usuario

**2. Capa de Controladores:**
- Archivo: `app.py`
- Responsabilidad: Manejar peticiones HTTP, validación básica, routing
- Ejemplo:
```python
@app.route('/docente/dashboard')
@requiere_autenticacion
@requiere_rol('docente')
def docente_dashboard():
    usuario = auth_service.obtener_usuario_actual()
    resumen = docente_service.obtener_resumen_dashboard(usuario['id'])
    return render_template('docente/dashboard.html', usuario=usuario, resumen=resumen)
```

**3. Capa de Servicios:**
- Archivos: `app/services/*.py`
- Responsabilidad: Lógica de negocio, orquestación de operaciones
- Ejemplo: `docente_service.py` coordina operaciones entre múltiples repositorios

**4. Capa de Repositorios:**
- Archivos: `app/repositories/*.py`
- Responsabilidad: Acceso a datos, operaciones CRUD
- Patrón Repository aplicado

**5. Capa de Modelos:**
- Archivos: `app/models/*.py`
- Responsabilidad: Representación de entidades del dominio
- Encapsulación de datos y comportamientos básicos

**6. Capa de Acceso a Datos:**
- Archivo: `app/patterns/singleton.py`
- Responsabilidad: Gestión de conexiones a la base de datos
- Patrón Singleton aplicado

### 1.2 Patrón MVC (Model-View-Controller)

El sistema implementa una variante del patrón MVC adaptado a Flask:

**MODEL (Modelo):**
- Ubicación: `app/models/`
- Archivos:
  - `usuario.py`: Clases Docente y Administrativo
  - `materia.py`: Clase Materia
  - `preferencia.py`: Clase Preferencia
  - `notificacion.py`: Clase Notificacion

Ejemplo de Modelo:
```python
class Docente:
    def __init__(self, id=None, nombre_completo='', email='', password_hash='',
                 telefono='', oficina='', departamento='', especialidad='', biografia=''):
        self.id = id
        self.nombre_completo = nombre_completo
        self.email = email
        self.password_hash = password_hash
        self.telefono = telefono
        self.oficina = oficina
        self.departamento = departamento
        self.especialidad = especialidad
        self.biografia = biografia
```

**VIEW (Vista):**
- Ubicación: `app/templates/`
- Estructura:
  - `auth/`: Vistas de autenticación
  - `docente/`: Vistas para docentes
  - `administrativo/`: Vistas para administrativos

Ejemplo de Vista:
```html
<!-- app/templates/docente/dashboard.html -->
<div class="stats-grid">
    <div class="stat-card">
        <h3>{{ resumen.materias_asignadas }}</h3>
        <p>Materias Asignadas</p>
    </div>
</div>
```

**CONTROLLER (Controlador):**
- Ubicación: `app.py` (rutas Flask)
- Responsabilidades:
  - Recibir peticiones HTTP
  - Invocar servicios de negocio
  - Retornar vistas con datos

Ejemplo de Controlador:
```python
@app.route('/docente/asignaturas')
@requiere_autenticacion
@requiere_rol('docente')
def docente_asignaturas():
    usuario = auth_service.obtener_usuario_actual()
    materias = docente_service.obtener_materias_asignadas(usuario['id'])
    return render_template('docente/asignaturas.html', materias=materias)
```

---

## 2. PATRONES DE DISEÑO IMPLEMENTADOS

### 2.1 Singleton Pattern

**Ubicación:** `app/patterns/singleton.py`

**Propósito:** Garantizar que solo exista una instancia de la conexión a la base de datos en toda la aplicación.

**Implementación:**

```python
class DatabaseConnection:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def connect(self, db_path):
        if self._connection is None:
            self._connection = sqlite3.connect(db_path, check_same_thread=False)
            self._connection.row_factory = sqlite3.Row
        return self._connection

    def get_connection(self):
        return self._connection
```

**Beneficios:**
- Control centralizado de la conexión a la base de datos
- Ahorro de recursos (una sola conexión)
- Prevención de conflictos de concurrencia
- Facilita el testing y mantenimiento

**Uso en el sistema:**
```python
# app.py
db = DatabaseConnection()
db.connect(app.config['DATABASE'])
```

### 2.2 Repository Pattern

**Ubicación:** `app/repositories/*.py`

**Propósito:** Abstraer el acceso a datos y desacoplar la lógica de negocio de la persistencia.

**Implementación:**

```python
class UsuarioRepository:
    def __init__(self, db_connection):
        self.db = db_connection

    def obtener_por_id(self, usuario_id, tipo):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        if tipo == 'docente':
            query = "SELECT * FROM docentes WHERE id = ?"
        else:
            query = "SELECT * FROM administrativos WHERE id = ?"

        cursor.execute(query, (usuario_id,))
        return cursor.fetchone()

    def crear(self, usuario, tipo):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        # Lógica de inserción
        conn.commit()

    def actualizar(self, usuario, tipo):
        # Lógica de actualización
        pass

    def eliminar(self, usuario_id, tipo):
        # Lógica de eliminación
        pass
```

**Beneficios:**
- Separación de responsabilidades
- Facilita testing con mocks
- Centraliza lógica de acceso a datos
- Permite cambiar el motor de BD sin afectar la lógica de negocio

**Repositorios implementados:**
1. `UsuarioRepository`: Gestión de docentes y administrativos
2. `MateriaRepository`: Gestión de materias
3. `HorarioRepository`: Gestión de horarios
4. `PreferenciaRepository`: Gestión de preferencias de docentes
5. `NotificacionRepository`: Gestión de notificaciones

### 2.3 Service Layer Pattern

**Ubicación:** `app/services/*.py`

**Propósito:** Encapsular la lógica de negocio compleja y orquestar operaciones entre múltiples repositorios.

**Implementación:**

```python
class DocenteService:
    def __init__(self, usuario_repo, materia_repo, preferencia_repo,
                 horario_repo, notificacion_repo):
        self.usuario_repo = usuario_repo
        self.materia_repo = materia_repo
        self.preferencia_repo = preferencia_repo
        self.horario_repo = horario_repo
        self.notificacion_repo = notificacion_repo

    def obtener_resumen_dashboard(self, docente_id):
        materias = self.materia_repo.obtener_por_docente(docente_id)
        preferencias = self.preferencia_repo.obtener_por_docente(docente_id)

        return {
            'materias_asignadas': len(materias),
            'preferencias_registradas': len(preferencias),
            'horarios_semanales': self._calcular_horas_semanales(docente_id)
        }

    def crear_preferencia(self, docente_id, materia_id, dia_semana, horario):
        if self._validar_disponibilidad(docente_id, dia_semana, horario):
            preferencia = Preferencia(
                docente_id=docente_id,
                materia_id=materia_id,
                dia_semana=dia_semana,
                horario=horario
            )
            self.preferencia_repo.crear(preferencia)
            return True, "Preferencia creada exitosamente"
        return False, "El horario no está disponible"
```

**Beneficios:**
- Lógica de negocio centralizada
- Reutilización de código
- Transacciones complejas coordinadas
- Facilita testing unitario

**Servicios implementados:**
1. `AuthService`: Autenticación y autorización
2. `DocenteService`: Operaciones específicas de docentes
3. `AdministrativoService`: Operaciones administrativas

### 2.4 Decorator Pattern

**Ubicación:** `app.py`

**Propósito:** Agregar funcionalidad a las rutas sin modificar su código (autenticación, autorización).

**Implementación:**

```python
def requiere_autenticacion(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if not auth_service.esta_autenticado():
            flash('Debes iniciar sesión para acceder', 'warning')
            return redirect(url_for('login_docente'))
        return f(*args, **kwargs)
    return decorador

def requiere_rol(rol_requerido):
    def decorador_rol(f):
        @wraps(f)
        def decorador(*args, **kwargs):
            if not auth_service.tiene_rol(rol_requerido):
                flash(f'Acceso denegado. Se requiere rol: {rol_requerido}', 'danger')
                return redirect(url_for('login_docente'))
            return f(*args, **kwargs)
        return decorador
    return decorador_rol
```

**Uso:**
```python
@app.route('/docente/dashboard')
@requiere_autenticacion
@requiere_rol('docente')
def docente_dashboard():
    # Código de la ruta
    pass
```

**Beneficios:**
- Separación de concerns (autenticación vs lógica de negocio)
- Código más limpio y legible
- Reutilización de lógica de seguridad
- Fácil de testear

### 2.5 Factory Method Pattern (Implícito)

**Ubicación:** `app/repositories/usuario_repository.py`

**Propósito:** Crear instancias de objetos sin especificar la clase exacta.

**Implementación:**

```python
def obtener_por_email(self, email, tipo):
    conn = self.db.get_connection()
    cursor = conn.cursor()

    if tipo == 'docente':
        cursor.execute("SELECT * FROM docentes WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row:
            return Docente(
                id=row['id'],
                nombre_completo=row['nombre_completo'],
                email=row['email'],
                password_hash=row['password_hash'],
                # ... otros campos
            )
    elif tipo == 'administrativo':
        cursor.execute("SELECT * FROM administrativos WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row:
            return Administrativo(
                id=row['id'],
                nombre_completo=row['nombre_completo'],
                email=row['email'],
                password_hash=row['password_hash'],
                # ... otros campos
            )

    return None
```

**Beneficios:**
- Encapsulación de la creación de objetos
- Flexibilidad para crear diferentes tipos de usuarios
- Código más mantenible

---

## 3. PRINCIPIOS SOLID

### 3.1 Single Responsibility Principle (SRP)

**Definición:** Una clase debe tener una sola razón para cambiar.

**Implementación en el sistema:**

**Ejemplo 1: Separación de Repositorios**
```python
# ❌ MAL - Una clase hace todo
class DataManager:
    def crear_usuario(self):
        pass
    def crear_materia(self):
        pass
    def crear_preferencia(self):
        pass
    def crear_notificacion(self):
        pass

# ✅ BIEN - Cada clase tiene una responsabilidad
class UsuarioRepository:
    def crear(self, usuario):
        pass
    def actualizar(self, usuario):
        pass
    def eliminar(self, usuario_id):
        pass

class MateriaRepository:
    def crear(self, materia):
        pass
    def actualizar(self, materia):
        pass
    def eliminar(self, materia_id):
        pass
```

**Ejemplo 2: Servicios especializados**
```python
# app/services/auth_service.py
class AuthService:
    # Responsabilidad: Solo autenticación y autorización
    def iniciar_sesion(self, email, password):
        pass

    def cerrar_sesion(self):
        pass

    def esta_autenticado(self):
        pass

# app/services/docente_service.py
class DocenteService:
    # Responsabilidad: Solo lógica de negocio de docentes
    def obtener_resumen_dashboard(self, docente_id):
        pass

    def obtener_materias_asignadas(self, docente_id):
        pass
```

**Beneficios aplicados:**
- Fácil mantenimiento
- Testing simplificado
- Cambios localizados

### 3.2 Open/Closed Principle (OCP)

**Definición:** Las entidades deben estar abiertas para extensión pero cerradas para modificación.

**Implementación en el sistema:**

**Ejemplo 1: Extensibilidad de Usuarios**
```python
# app/models/usuario.py
class Usuario:
    def __init__(self, id, nombre_completo, email, password_hash):
        self.id = id
        self.nombre_completo = nombre_completo
        self.email = email
        self.password_hash = password_hash

# Extensión sin modificar la clase base
class Docente(Usuario):
    def __init__(self, id=None, nombre_completo='', email='', password_hash='',
                 telefono='', oficina='', departamento='', especialidad=''):
        super().__init__(id, nombre_completo, email, password_hash)
        self.telefono = telefono
        self.oficina = oficina
        self.departamento = departamento
        self.especialidad = especialidad

class Administrativo(Usuario):
    def __init__(self, id=None, nombre_completo='', email='', password_hash='',
                 telefono='', area=''):
        super().__init__(id, nombre_completo, email, password_hash)
        self.telefono = telefono
        self.area = area
```

**Ejemplo 2: Decoradores extensibles**
```python
# Puedes agregar nuevos decoradores sin modificar los existentes
@app.route('/docente/dashboard')
@requiere_autenticacion
@requiere_rol('docente')
# Fácil agregar: @cache, @rate_limit, @log_access, etc.
def docente_dashboard():
    pass
```

**Beneficios aplicados:**
- Nuevas funcionalidades sin romper código existente
- Sistema extensible y flexible

### 3.3 Liskov Substitution Principle (LSP)

**Definición:** Los objetos de una subclase deben poder reemplazar a los de su superclase sin alterar el comportamiento.

**Implementación en el sistema:**

**Ejemplo 1: Polimorfismo en Repositorios**
```python
# Cualquier repositorio puede usarse de forma intercambiable
class BaseRepository:
    def obtener_por_id(self, id):
        raise NotImplementedError

    def crear(self, entidad):
        raise NotImplementedError

    def actualizar(self, entidad):
        raise NotImplementedError

    def eliminar(self, id):
        raise NotImplementedError

class UsuarioRepository(BaseRepository):
    def obtener_por_id(self, id, tipo):
        # Implementación específica
        pass

class MateriaRepository(BaseRepository):
    def obtener_por_id(self, id):
        # Implementación específica
        pass
```

**Ejemplo 2: Usuarios intercambiables**
```python
def validar_email(usuario):
    # Funciona con Docente o Administrativo
    return '@' in usuario.email

docente = Docente(email='docente@demo.com')
admin = Administrativo(email='admin@demo.com')

validar_email(docente)  # ✅ Funciona
validar_email(admin)    # ✅ Funciona
```

**Beneficios aplicados:**
- Código más flexible y reutilizable
- Facilita testing con mocks

### 3.4 Interface Segregation Principle (ISP)

**Definición:** Los clientes no deben depender de interfaces que no usan.

**Implementación en el sistema:**

**Ejemplo 1: Servicios específicos**
```python
# ❌ MAL - Interface gigante
class UsuarioService:
    def obtener_dashboard_docente(self):
        pass
    def obtener_dashboard_admin(self):
        pass
    def crear_docente(self):
        pass
    def crear_admin(self):
        pass
    # Docentes no necesitan métodos de admin y viceversa

# ✅ BIEN - Interfaces segregadas
class DocenteService:
    def obtener_resumen_dashboard(self, docente_id):
        pass

    def obtener_materias_asignadas(self, docente_id):
        pass

    def crear_preferencia(self, docente_id, materia_id, dia, horario):
        pass

class AdministrativoService:
    def obtener_resumen_dashboard(self):
        pass

    def obtener_docentes(self):
        pass

    def asignar_materia_docente(self, materia_id, docente_id):
        pass
```

**Ejemplo 2: Repositorios específicos**
```python
# Cada repositorio expone solo métodos relevantes
class PreferenciaRepository:
    def obtener_por_docente(self, docente_id):
        pass

    def crear(self, preferencia):
        pass

    def eliminar(self, preferencia_id):
        pass
    # No tiene métodos irrelevantes como 'obtener_por_admin'
```

**Beneficios aplicados:**
- Interfaces más limpias
- Menos acoplamiento
- Código más fácil de entender

### 3.5 Dependency Inversion Principle (DIP)

**Definición:** Depender de abstracciones, no de concreciones.

**Implementación en el sistema:**

**Ejemplo 1: Inyección de dependencias en Servicios**
```python
# app/services/docente_service.py
class DocenteService:
    # ✅ Depende de abstracciones (repositorios), no de implementaciones concretas
    def __init__(self, usuario_repo, materia_repo, preferencia_repo,
                 horario_repo, notificacion_repo):
        self.usuario_repo = usuario_repo
        self.materia_repo = materia_repo
        self.preferencia_repo = preferencia_repo
        self.horario_repo = horario_repo
        self.notificacion_repo = notificacion_repo

    def obtener_resumen_dashboard(self, docente_id):
        # Usa las abstracciones inyectadas
        materias = self.materia_repo.obtener_por_docente(docente_id)
        return {'materias_asignadas': len(materias)}
```

**Ejemplo 2: Inicialización con Inyección de Dependencias**
```python
# app.py
db = DatabaseConnection()
db.connect(app.config['DATABASE'])

# Creación de repositorios
usuario_repo = UsuarioRepository(db)
materia_repo = MateriaRepository(db)
preferencia_repo = PreferenciaRepository(db)
horario_repo = HorarioRepository(db)
notificacion_repo = NotificacionRepository(db)

# Inyección de dependencias en servicios
auth_service = AuthService(usuario_repo)
docente_service = DocenteService(
    usuario_repo,
    materia_repo,
    preferencia_repo,
    horario_repo,
    notificacion_repo
)
administrativo_service = AdministrativoService(
    usuario_repo,
    materia_repo,
    preferencia_repo,
    notificacion_repo
)
```

**Beneficios aplicados:**
- Facilita testing (puedes inyectar mocks)
- Bajo acoplamiento
- Alta cohesión
- Código más mantenible

**Ejemplo 3: Testing con DIP**
```python
# test_docente_service.py
class MockMateriaRepository:
    def obtener_por_docente(self, docente_id):
        return [Mock1(), Mock2()]

# Fácil crear test con mock
mock_repo = MockMateriaRepository()
service = DocenteService(usuario_repo=None, materia_repo=mock_repo, ...)
resumen = service.obtener_resumen_dashboard(1)
assert resumen['materias_asignadas'] == 2
```

---

## 4. RESUMEN DE BENEFICIOS

### Arquitectura en Capas:
- ✅ Separación clara de responsabilidades
- ✅ Facilita el mantenimiento
- ✅ Permite testing por capas
- ✅ Escalabilidad horizontal

### Patrones de Diseño:
- ✅ Singleton: Control de recursos compartidos
- ✅ Repository: Abstracción de datos
- ✅ Service Layer: Lógica de negocio centralizada
- ✅ Decorator: Funcionalidad transversal reutilizable
- ✅ Factory: Creación de objetos flexible

### Principios SOLID:
- ✅ SRP: Código modular y mantenible
- ✅ OCP: Sistema extensible
- ✅ LSP: Polimorfismo efectivo
- ✅ ISP: Interfaces limpias
- ✅ DIP: Bajo acoplamiento

---

## 5. DIAGRAMA DE DEPENDENCIAS

```
┌─────────────┐
│   app.py    │
│ (Controllers)│
└──────┬──────┘
       │
       ├─────────────────────────────────┐
       │                                 │
       ▼                                 ▼
┌──────────────┐                  ┌──────────────┐
│  Services    │                  │ Decorators   │
│              │                  │              │
│ - AuthService│                  │ - @requiere_ │
│ - Docente    │                  │   autentica  │
│ - Admin      │                  │ - @requiere_ │
└──────┬───────┘                  │   rol        │
       │                          └──────────────┘
       │
       ▼
┌──────────────┐
│ Repositories │
│              │
│ - Usuario    │
│ - Materia    │
│ - Preferencia│
│ - Horario    │
│ - Notificacion│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Models     │
│              │
│ - Docente    │
│ - Administrativo│
│ - Materia    │
│ - Preferencia│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Singleton   │
│              │
│ - Database   │
│   Connection │
└──────────────┘
```

---

## 6. CONCLUSIÓN

El sistema implementa una arquitectura robusta y escalable basada en:

1. **Arquitectura en Capas** que separa claramente las responsabilidades
2. **Patrones de Diseño** probados que facilitan el mantenimiento
3. **Principios SOLID** que garantizan código limpio y extensible

Esta combinación resulta en un sistema:
- Fácil de testear
- Fácil de mantener
- Fácil de extender
- Robusto y confiable
- Preparado para pruebas de calidad

---

**Versión:** 1.0
