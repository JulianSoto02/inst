"""
Repositorio de Usuarios
Implementa el patrón Repository para acceso a datos de usuarios.
Aplica principios SOLID (SRP, DIP, ISP).
"""

from typing import List, Optional
from application.patterns.repository import BaseRepository
from application.patterns.factory import UsuarioFactory
from application.models.user import Usuario, Docente, Administrativo
import hashlib


class UsuarioRepository(BaseRepository[Usuario]):
    """
    Repositorio para gestionar usuarios (Docentes y Administrativos).

    Patrón: Repository
    Principios SOLID:
    - SRP: Responsabilidad única de acceso a datos de usuarios
    - DIP: Depende de abstracción (BaseRepository)
    """

    def _get_table_name(self) -> str:
        return "usuarios"

    def _map_to_entity(self, row) -> Optional[Usuario]:
        """No se usa en este caso ya que tenemos tablas separadas"""
        return None

    def obtener_por_id(self, id: int, rol: str) -> Optional[Usuario]:
        """
        Obtiene un usuario por ID y rol.

        Args:
            id: ID del usuario
            rol: Rol del usuario ('docente' o 'administrativo')

        Returns:
            Instancia de Usuario o None
        """
        tabla = "docentes" if rol.lower() == "docente" else "administrativos"
        cursor = self._db.get_connection().cursor()
        cursor.execute(f"SELECT * FROM {tabla} WHERE id = ?", (id,))
        row = cursor.fetchone()

        if row:
            return UsuarioFactory.crear_desde_db(rol, row)
        return None

    def obtener_por_email(self, email: str) -> Optional[tuple[Usuario, str]]:
        """
        Obtiene un usuario por email, buscando en ambas tablas.

        Args:
            email: Email del usuario

        Returns:
            Tupla (usuario, rol) o None
        """
        # Buscar en docentes
        cursor = self._db.get_connection().cursor()
        cursor.execute("SELECT * FROM docentes WHERE email = ?", (email,))
        row = cursor.fetchone()

        if row:
            usuario = UsuarioFactory.crear_desde_db('docente', row)
            return (usuario, 'docente')

        # Buscar en administrativos
        cursor.execute("SELECT * FROM administrativos WHERE email = ?", (email,))
        row = cursor.fetchone()

        if row:
            usuario = UsuarioFactory.crear_desde_db('administrativo', row)
            return (usuario, 'administrativo')

        return None

    def crear(self, usuario: Usuario) -> Usuario:
        """
        Crea un nuevo usuario en la base de datos.

        Args:
            usuario: Instancia de Usuario a crear

        Returns:
            Usuario con ID asignado
        """
        conn = self._db.get_connection()
        cursor = conn.cursor()

        # Hash de la contraseña
        password_hash = self._hash_password(usuario.password)

        if isinstance(usuario, Docente):
            cursor.execute("""
                INSERT INTO docentes (nombre_completo, email, password, telefono,
                                     oficina, departamento, especialidad, biografia, activo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (usuario.nombre_completo, usuario.email, password_hash,
                  usuario.telefono, usuario.oficina, usuario.departamento,
                  usuario.especialidad, usuario.biografia, 1))

        elif isinstance(usuario, Administrativo):
            cursor.execute("""
                INSERT INTO administrativos (nombre_completo, email, password, telefono,
                                            oficina, departamento, cargo, biografia, activo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (usuario.nombre_completo, usuario.email, password_hash,
                  usuario.telefono, usuario.oficina, usuario.departamento,
                  usuario.cargo, usuario.biografia, 1))

        conn.commit()
        usuario.id = cursor.lastrowid
        return usuario

    def actualizar(self, usuario: Usuario) -> bool:
        """
        Actualiza un usuario existente.

        Args:
            usuario: Usuario con datos actualizados

        Returns:
            True si se actualizó correctamente
        """
        conn = self._db.get_connection()
        cursor = conn.cursor()

        if isinstance(usuario, Docente):
            cursor.execute("""
                UPDATE docentes
                SET nombre_completo = ?, email = ?, telefono = ?, oficina = ?,
                    departamento = ?, especialidad = ?, biografia = ?
                WHERE id = ?
            """, (usuario.nombre_completo, usuario.email, usuario.telefono,
                  usuario.oficina, usuario.departamento, usuario.especialidad,
                  usuario.biografia, usuario.id))

        elif isinstance(usuario, Administrativo):
            cursor.execute("""
                UPDATE administrativos
                SET nombre_completo = ?, email = ?, telefono = ?, oficina = ?,
                    departamento = ?, cargo = ?, biografia = ?
                WHERE id = ?
            """, (usuario.nombre_completo, usuario.email, usuario.telefono,
                  usuario.oficina, usuario.departamento, usuario.cargo,
                  usuario.biografia, usuario.id))

        conn.commit()
        return cursor.rowcount > 0

    def actualizar_password(self, usuario_id: int, nueva_password: str, rol: str) -> bool:
        """
        Actualiza la contraseña de un usuario.

        Args:
            usuario_id: ID del usuario
            nueva_password: Nueva contraseña
            rol: Rol del usuario

        Returns:
            True si se actualizó correctamente
        """
        conn = self._db.get_connection()
        cursor = conn.cursor()

        password_hash = self._hash_password(nueva_password)
        tabla = "docentes" if rol.lower() == "docente" else "administrativos"

        cursor.execute(f"UPDATE {tabla} SET password = ? WHERE id = ?",
                      (password_hash, usuario_id))
        conn.commit()
        return cursor.rowcount > 0

    def eliminar(self, id: int, rol: str) -> bool:
        """
        Elimina (desactiva) un usuario.

        Args:
            id: ID del usuario
            rol: Rol del usuario

        Returns:
            True si se eliminó correctamente
        """
        conn = self._db.get_connection()
        cursor = conn.cursor()

        tabla = "docentes" if rol.lower() == "docente" else "administrativos"
        cursor.execute(f"UPDATE {tabla} SET activo = 0 WHERE id = ?", (id,))
        conn.commit()
        return cursor.rowcount > 0

    def obtener_todos(self) -> List[Usuario]:
        """Obtiene todos los usuarios (docentes y administrativos)"""
        usuarios = []

        # Obtener docentes
        cursor = self._db.get_connection().cursor()
        cursor.execute("SELECT * FROM docentes WHERE activo = 1")
        for row in cursor.fetchall():
            usuarios.append(UsuarioFactory.crear_desde_db('docente', row))

        # Obtener administrativos
        cursor.execute("SELECT * FROM administrativos WHERE activo = 1")
        for row in cursor.fetchall():
            usuarios.append(UsuarioFactory.crear_desde_db('administrativo', row))

        return usuarios

    def obtener_docentes(self) -> List[Docente]:
        """Obtiene todos los docentes activos"""
        cursor = self._db.get_connection().cursor()
        cursor.execute("SELECT * FROM docentes WHERE activo = 1")
        return [UsuarioFactory.crear_desde_db('docente', row) for row in cursor.fetchall()]

    def obtener_administrativos(self) -> List[Administrativo]:
        """Obtiene todos los administrativos activos"""
        cursor = self._db.get_connection().cursor()
        cursor.execute("SELECT * FROM administrativos WHERE activo = 1")
        return [UsuarioFactory.crear_desde_db('administrativo', row) for row in cursor.fetchall()]

    @staticmethod
    def _hash_password(password: str) -> str:
        """
        Genera hash de contraseña usando SHA-256.

        Args:
            password: Contraseña en texto plano

        Returns:
            Hash de la contraseña
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def verificar_credenciales(self, email: str, password: str) -> Optional[tuple[Usuario, str]]:
        """
        Verifica las credenciales de un usuario.

        Args:
            email: Email del usuario
            password: Contraseña en texto plano

        Returns:
            Tupla (usuario, rol) si las credenciales son válidas, None en caso contrario
        """
        resultado = self.obtener_por_email(email)

        if resultado:
            usuario, rol = resultado
            password_hash = self._hash_password(password)

            # Verificar password
            tabla = "docentes" if rol == "docente" else "administrativos"
            cursor = self._db.get_connection().cursor()
            cursor.execute(f"SELECT password FROM {tabla} WHERE id = ?", (usuario.id,))
            row = cursor.fetchone()

            if row and row[0] == password_hash:
                return (usuario, rol)

        return None
