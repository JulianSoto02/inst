"""
PATRÓN REPOSITORY (Arquitectural)
=================================
Encapsula la lógica de acceso a datos y proporciona una interfaz similar
a una colección para acceder a objetos del dominio.

Ventajas:
- Separa la lógica de negocio de la lógica de acceso a datos
- Centraliza consultas comunes
- Facilita el testing (se puede mockear)
- Permite cambiar la fuente de datos sin afectar la lógica de negocio

Uso en el sistema:
- Acceso a datos de usuarios, materias, preferencias, notificaciones
- Abstracción de operaciones CRUD
- Implementación de principio DIP (Inversión de Dependencias)
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Generic, TypeVar


T = TypeVar('T')


class IRepository(ABC, Generic[T]):
    """
    Interfaz genérica de Repository.

    Patrón: Repository
    Principios SOLID aplicados:
    - ISP: Interfaz segregada con operaciones básicas
    - DIP: Los servicios dependen de esta abstracción
    - OCP: Abierto para extensión con repositorios específicos
    """

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[T]:
        """Obtiene una entidad por su ID"""
        pass

    @abstractmethod
    def obtener_todos(self) -> List[T]:
        """Obtiene todas las entidades"""
        pass

    @abstractmethod
    def crear(self, entidad: T) -> T:
        """Crea una nueva entidad"""
        pass

    @abstractmethod
    def actualizar(self, entidad: T) -> bool:
        """Actualiza una entidad existente"""
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina una entidad por su ID"""
        pass


class BaseRepository(IRepository[T], ABC):
    """
    Repositorio base con implementación común.

    Principio SRP: Responsabilidad de operaciones CRUD básicas.
    Template Method: Define estructura que subclases implementan.
    """

    def __init__(self, db_connection):
        """
        Args:
            db_connection: Conexión a la base de datos (Singleton)
        """
        self._db = db_connection

    @abstractmethod
    def _get_table_name(self) -> str:
        """Devuelve el nombre de la tabla"""
        pass

    @abstractmethod
    def _map_to_entity(self, row) -> T:
        """Mapea una fila de BD a una entidad"""
        pass

    def obtener_todos(self) -> List[T]:
        """Implementación genérica de obtener todos"""
        cursor = self._db.get_connection().cursor()
        cursor.execute(f"SELECT * FROM {self._get_table_name()}")
        rows = cursor.fetchall()
        return [self._map_to_entity(row) for row in rows]

    def obtener_por_id(self, id: int) -> Optional[T]:
        """Implementación genérica de obtener por ID"""
        cursor = self._db.get_connection().cursor()
        cursor.execute(f"SELECT * FROM {self._get_table_name()} WHERE id = ?", (id,))
        row = cursor.fetchone()
        return self._map_to_entity(row) if row else None


# Este patrón se implementará completamente en los repositorios específicos
# (repositories/usuario_repository.py, etc.)

# Ejemplo de estructura:
"""
class UsuarioRepository(BaseRepository[Usuario]):
    def _get_table_name(self) -> str:
        return "usuarios"

    def _map_to_entity(self, row) -> Usuario:
        # Mapeo específico de usuario
        pass

    def crear(self, usuario: Usuario) -> Usuario:
        # Implementación específica
        pass

    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        # Método específico de usuario
        pass
"""
