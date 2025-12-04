"""
Servicio de Autenticación
Capa de Negocio - Gestiona la autenticación y autorización de usuarios.

Principios SOLID aplicados:
- SRP: Responsabilidad única de autenticación
- DIP: Depende de abstracciones (Repository)
- OCP: Abierto para extensión (nuevos métodos de autenticación)
"""

from typing import Optional, Dict
from app.repositories.usuario_repository import UsuarioRepository
from app.patterns.singleton import SessionManager
from app.models.user import Usuario


class AuthService:
    """
    Servicio de autenticación y gestión de sesiones.

    Aplica principio SRP: Única responsabilidad de autenticación.
    Aplica principio DIP: Depende de UsuarioRepository (abstracción).
    """

    def __init__(self, usuario_repository: UsuarioRepository):
        """
        Args:
            usuario_repository: Repositorio de usuarios
        """
        self._usuario_repo = usuario_repository
        self._session_manager = SessionManager()

    def iniciar_sesion(self, email: str, password: str) -> tuple[bool, Optional[str], Optional[Dict]]:
        """
        Autentica un usuario y crea una sesión.

        Args:
            email: Email del usuario
            password: Contraseña

        Returns:
            Tupla (exito, mensaje, datos_usuario)
        """
        # Verificar credenciales
        resultado = self._usuario_repo.verificar_credenciales(email, password)

        if not resultado:
            return (False, "Credenciales inválidas", None)

        usuario, rol = resultado

        # Crear sesión
        datos_sesion = {
            'id': usuario.id,
            'nombre_completo': usuario.nombre_completo,
            'email': usuario.email,
            'rol': rol,
            'telefono': usuario.telefono,
            'oficina': usuario.oficina
        }

        self._session_manager.crear_sesion(usuario.id, datos_sesion)

        return (True, "Inicio de sesión exitoso", datos_sesion)

    def cerrar_sesion(self) -> bool:
        """
        Cierra la sesión actual.

        Returns:
            True si se cerró correctamente
        """
        self._session_manager.cerrar_sesion()
        return True

    def obtener_usuario_actual(self) -> Optional[Dict]:
        """
        Obtiene los datos del usuario en sesión.

        Returns:
            Diccionario con datos del usuario o None
        """
        return self._session_manager.obtener_sesion_actual()

    def esta_autenticado(self) -> bool:
        """
        Verifica si hay un usuario autenticado.

        Returns:
            True si hay sesión activa
        """
        return self._session_manager.hay_sesion_activa()

    def tiene_rol(self, rol_requerido: str) -> bool:
        """
        Verifica si el usuario actual tiene un rol específico.

        Args:
            rol_requerido: Rol a verificar ('docente' o 'administrativo')

        Returns:
            True si el usuario tiene el rol
        """
        usuario = self.obtener_usuario_actual()
        if not usuario:
            return False

        return usuario.get('rol', '').lower() == rol_requerido.lower()

    def cambiar_password(self, password_actual: str, password_nueva: str) -> tuple[bool, str]:
        """
        Cambia la contraseña del usuario actual.

        Args:
            password_actual: Contraseña actual
            password_nueva: Nueva contraseña

        Returns:
            Tupla (exito, mensaje)
        """
        usuario = self.obtener_usuario_actual()
        if not usuario:
            return (False, "No hay sesión activa")

        # Verificar password actual
        resultado = self._usuario_repo.verificar_credenciales(
            usuario['email'],
            password_actual
        )

        if not resultado:
            return (False, "Contraseña actual incorrecta")

        # Actualizar password
        exito = self._usuario_repo.actualizar_password(
            usuario['id'],
            password_nueva,
            usuario['rol']
        )

        if exito:
            return (True, "Contraseña actualizada correctamente")
        else:
            return (False, "Error al actualizar contraseña")
