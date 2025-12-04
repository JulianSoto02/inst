"""
PATRÓN FACTORY (Creacional)
==========================
Proporciona una interfaz para crear objetos sin especificar sus clases concretas.

Ventajas:
- Centraliza la lógica de creación de objetos
- Facilita la extensión con nuevos tipos
- Aplica principios SOLID (OCP, DIP)

Uso en el sistema:
- Crear diferentes tipos de usuarios (Docente, Administrativo)
- Permite agregar nuevos roles sin modificar código existente
"""

from typing import Optional, Dict
from app.models.user import Usuario, Docente, Administrativo


class UsuarioFactory:
    """
    Factory para crear instancias de diferentes tipos de usuarios.

    Patrón: Factory Method
    Principios SOLID aplicados:
    - OCP: Abierto para extensión (nuevos tipos), cerrado para modificación
    - DIP: Depende de la abstracción Usuario, no de implementaciones concretas
    """

    @staticmethod
    def crear_usuario(tipo: str, datos: Dict) -> Usuario:
        """
        Crea una instancia de usuario según el tipo especificado.

        Args:
            tipo: Tipo de usuario ('docente' o 'administrativo')
            datos: Diccionario con los datos del usuario

        Returns:
            Instancia de Usuario (Docente o Administrativo)

        Raises:
            ValueError: Si el tipo de usuario no es válido
        """
        tipo = tipo.lower()

        if tipo == 'docente':
            return UsuarioFactory._crear_docente(datos)
        elif tipo == 'administrativo':
            return UsuarioFactory._crear_administrativo(datos)
        else:
            raise ValueError(f"Tipo de usuario no válido: {tipo}")

    @staticmethod
    def _crear_docente(datos: Dict) -> Docente:
        """Crea una instancia de Docente"""
        return Docente(
            id=datos.get('id'),
            nombre_completo=datos['nombre_completo'],
            email=datos['email'],
            password=datos['password'],
            telefono=datos.get('telefono', ''),
            oficina=datos.get('oficina', ''),
            departamento=datos.get('departamento', ''),
            especialidad=datos.get('especialidad', ''),
            biografia=datos.get('biografia', '')
        )

    @staticmethod
    def _crear_administrativo(datos: Dict) -> Administrativo:
        """Crea una instancia de Administrativo"""
        return Administrativo(
            id=datos.get('id'),
            nombre_completo=datos['nombre_completo'],
            email=datos['email'],
            password=datos['password'],
            telefono=datos.get('telefono', ''),
            oficina=datos.get('oficina', ''),
            departamento=datos.get('departamento', ''),
            cargo=datos.get('cargo', 'Encargado de asignaciones'),
            biografia=datos.get('biografia', '')
        )

    @staticmethod
    def crear_desde_db(tipo: str, row: tuple) -> Usuario:
        """
        Crea un usuario a partir de una fila de base de datos.

        Args:
            tipo: Tipo de usuario
            row: Tupla con datos de la BD

        Returns:
            Instancia de Usuario
        """
        if tipo.lower() == 'docente':
            return Docente(
                id=row[0],
                nombre_completo=row[1],
                email=row[2],
                password=row[3],
                telefono=row[4] or '',
                oficina=row[5] or '',
                departamento=row[6] or '',
                especialidad=row[7] or '',
                biografia=row[8] or ''
            )
        elif tipo.lower() == 'administrativo':
            return Administrativo(
                id=row[0],
                nombre_completo=row[1],
                email=row[2],
                password=row[3],
                telefono=row[4] or '',
                oficina=row[5] or '',
                departamento=row[6] or '',
                cargo=row[7] or 'Encargado de asignaciones',
                biografia=row[8] or ''
            )
        else:
            raise ValueError(f"Tipo de usuario no válido: {tipo}")


# Ejemplo de uso:
"""
# Crear un docente
datos_docente = {
    'nombre_completo': 'Dr. Carlos Martínez',
    'email': 'docente@demo.com',
    'password': 'hashed_password',
    'telefono': '+52 555 123 4567',
    'oficina': 'Edificio A - Oficina 12',
    'departamento': 'Matemáticas',
    'especialidad': 'Cálculo y Análisis Matemático',
    'biografia': 'Doctor en Matemáticas con 15 años de experiencia...'
}

docente = UsuarioFactory.crear_usuario('docente', datos_docente)

# Crear un administrativo
datos_admin = {
    'nombre_completo': 'David Piedrahita',
    'email': 'administrativo@demo.com',
    'password': 'hashed_password',
    'telefono': '+52 525 876 3597',
    'oficina': 'Edificio A - Oficina 12',
    'departamento': 'Administrativo',
    'cargo': 'Encargado de asignaciones',
    'biografia': 'Profesional en Administración...'
}

admin = UsuarioFactory.crear_usuario('administrativo', datos_admin)
"""
