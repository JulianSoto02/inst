"""
PATRÓN SINGLETON (Creacional)
=============================
Garantiza que una clase tenga una única instancia y proporciona un punto de acceso global.

Ventajas:
- Control estricto sobre cómo y cuándo se accede a la instancia única
- Ahorro de recursos al evitar múltiples instancias
- Punto de acceso global controlado

Uso en el sistema:
- Gestión de sesiones de usuario
- Conexión a base de datos
- Configuración global de la aplicación
"""

import sqlite3
from typing import Optional
from threading import Lock


class DatabaseConnection:
    """
    Singleton para la conexión a la base de datos.

    Patrón: Singleton (Thread-Safe)
    Principios SOLID aplicados:
    - SRP: Única responsabilidad de gestionar la conexión a BD
    - DIP: Otros componentes dependen de esta abstracción
    """

    _instance: Optional['DatabaseConnection'] = None
    _lock: Lock = Lock()
    _connection: Optional[sqlite3.Connection] = None

    def __new__(cls):
        """
        Implementación thread-safe del Singleton.
        Usa double-checked locking para rendimiento.
        """
        if cls._instance is None:
            with cls._lock:
                # Double-checked locking
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Inicializa la conexión solo una vez"""
        # Solo inicializa si no se ha hecho antes
        if self._connection is None:
            self._connection = None
            self._db_path = "database/universidad.db"

    def connect(self, db_path: str = "database/universidad.db"):
        """
        Establece la conexión a la base de datos.

        Args:
            db_path: Ruta al archivo de base de datos SQLite
        """
        if self._connection is None:
            self._db_path = db_path
            self._connection = sqlite3.connect(db_path, check_same_thread=False)
            self._connection.row_factory = sqlite3.Row
            print(f"[OK] Conexion establecida con la base de datos: {db_path}")

    def get_connection(self) -> sqlite3.Connection:
        """
        Obtiene la conexión activa a la base de datos.

        Returns:
            Conexión SQLite activa

        Raises:
            RuntimeError: Si no se ha establecido la conexión
        """
        if self._connection is None:
            raise RuntimeError("No se ha establecido conexión con la base de datos")
        return self._connection

    def close(self):
        """Cierra la conexión a la base de datos"""
        if self._connection:
            self._connection.close()
            self._connection = None
            print("[OK] Conexion a base de datos cerrada")

    @classmethod
    def reset_instance(cls):
        """Resetea la instancia (útil para testing)"""
        with cls._lock:
            if cls._instance and cls._instance._connection:
                cls._instance._connection.close()
            cls._instance = None


class SessionManager:
    """
    Singleton para gestionar las sesiones de usuario.

    Patrón: Singleton
    Principios SOLID aplicados:
    - SRP: Única responsabilidad de gestionar sesiones
    """

    _instance: Optional['SessionManager'] = None
    _lock: Lock = Lock()

    def __new__(cls):
        """Implementación thread-safe del Singleton"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Inicializa el gestor de sesiones solo una vez"""
        if not hasattr(self, '_initialized'):
            self._sessions = {}  # user_id -> user_data
            self._current_user_id = None
            self._initialized = True

    def crear_sesion(self, user_id: int, user_data: dict):
        """
        Crea una nueva sesión para un usuario.

        Args:
            user_id: ID del usuario
            user_data: Datos del usuario a almacenar en sesión
        """
        self._sessions[user_id] = user_data
        self._current_user_id = user_id
        print(f"[OK] Sesion creada para usuario: {user_data.get('nombre_completo')}")

    def obtener_sesion_actual(self) -> Optional[dict]:
        """
        Obtiene los datos de la sesión actual.

        Returns:
            Datos del usuario en sesión o None
        """
        if self._current_user_id:
            return self._sessions.get(self._current_user_id)
        return None

    def obtener_usuario_actual_id(self) -> Optional[int]:
        """
        Obtiene el ID del usuario actual.

        Returns:
            ID del usuario o None
        """
        return self._current_user_id

    def cerrar_sesion(self):
        """Cierra la sesión actual"""
        if self._current_user_id:
            user_data = self._sessions.get(self._current_user_id)
            if user_data:
                print(f"[OK] Sesion cerrada para: {user_data.get('nombre_completo')}")
            del self._sessions[self._current_user_id]
            self._current_user_id = None

    def hay_sesion_activa(self) -> bool:
        """
        Verifica si hay una sesión activa.

        Returns:
            True si hay sesión activa, False en caso contrario
        """
        return self._current_user_id is not None

    @classmethod
    def reset_instance(cls):
        """Resetea la instancia (útil para testing)"""
        with cls._lock:
            cls._instance = None


# Ejemplo de uso:
"""
# Obtener instancia de conexión a BD (siempre la misma)
db1 = DatabaseConnection()
db1.connect("database/universidad.db")

db2 = DatabaseConnection()  # Devuelve la misma instancia
assert db1 is db2  # True

# Gestión de sesiones
session_mgr1 = SessionManager()
session_mgr1.crear_sesion(1, {'nombre': 'Dr. Carlos', 'rol': 'Docente'})

session_mgr2 = SessionManager()  # Devuelve la misma instancia
assert session_mgr1 is session_mgr2  # True
assert session_mgr2.hay_sesion_activa()  # True
"""
