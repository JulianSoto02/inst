"""
Modelos de Usuario - Capa de Datos
Aplica principios SOLID:
- SRP: Cada clase tiene una única responsabilidad
- OCP: Abierto para extensión (herencia), cerrado para modificación
- LSP: Las subclases pueden sustituir a la clase base
- ISP: Interfaces segregadas por tipo de usuario
- DIP: Depende de abstracciones (clase base abstracta)
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List, Dict


class Usuario(ABC):
    """
    Clase base abstracta para todos los usuarios del sistema.
    Principio DIP: Dependencia de abstracción.
    """

    def __init__(self, id: Optional[int], nombre_completo: str,
                 email: str, password: str, telefono: str, oficina: str):
        self._id = id
        self._nombre_completo = nombre_completo
        self._email = email
        self._password = password
        self._telefono = telefono
        self._oficina = oficina
        self._fecha_creacion = datetime.now()
        self._activo = True

    # Getters y Setters (Encapsulación)
    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def nombre_completo(self) -> str:
        return self._nombre_completo

    @nombre_completo.setter
    def nombre_completo(self, value: str):
        self._nombre_completo = value

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        self._email = value

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str):
        self._password = value

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, value: str):
        self._telefono = value

    @property
    def oficina(self) -> str:
        return self._oficina

    @oficina.setter
    def oficina(self, value: str):
        self._oficina = value

    @property
    def activo(self) -> bool:
        return self._activo

    @activo.setter
    def activo(self, value: bool):
        self._activo = value

    @abstractmethod
    def get_rol(self) -> str:
        """Método abstracto que debe ser implementado por subclases"""
        pass

    @abstractmethod
    def to_dict(self) -> Dict:
        """Convierte el usuario a diccionario"""
        pass

    def __str__(self) -> str:
        return f"{self.get_rol()}: {self._nombre_completo} ({self._email})"


class Docente(Usuario):
    """
    Clase Docente - Hereda de Usuario.
    Principio LSP: Puede sustituir a Usuario en cualquier contexto.
    Principio SRP: Responsabilidad única de representar un docente.
    """

    def __init__(self, id: Optional[int], nombre_completo: str, email: str,
                 password: str, telefono: str, oficina: str,
                 departamento: str, especialidad: str, biografia: str):
        super().__init__(id, nombre_completo, email, password, telefono, oficina)
        self._departamento = departamento
        self._especialidad = especialidad
        self._biografia = biografia
        self._materias_asignadas: List['Materia'] = []

    @property
    def departamento(self) -> str:
        return self._departamento

    @departamento.setter
    def departamento(self, value: str):
        self._departamento = value

    @property
    def especialidad(self) -> str:
        return self._especialidad

    @especialidad.setter
    def especialidad(self, value: str):
        self._especialidad = value

    @property
    def biografia(self) -> str:
        return self._biografia

    @biografia.setter
    def biografia(self, value: str):
        self._biografia = value

    @property
    def materias_asignadas(self) -> List['Materia']:
        return self._materias_asignadas

    def agregar_materia(self, materia: 'Materia'):
        """Agrega una materia al docente"""
        if materia not in self._materias_asignadas:
            self._materias_asignadas.append(materia)

    def get_rol(self) -> str:
        return "Docente"

    def to_dict(self) -> Dict:
        return {
            'id': self._id,
            'nombre_completo': self._nombre_completo,
            'email': self._email,
            'telefono': self._telefono,
            'oficina': self._oficina,
            'departamento': self._departamento,
            'especialidad': self._especialidad,
            'biografia': self._biografia,
            'rol': self.get_rol(),
            'activo': self._activo
        }


class Administrativo(Usuario):
    """
    Clase Administrativo - Hereda de Usuario.
    Principio LSP: Puede sustituir a Usuario en cualquier contexto.
    Principio SRP: Responsabilidad única de representar un administrativo.
    """

    def __init__(self, id: Optional[int], nombre_completo: str, email: str,
                 password: str, telefono: str, oficina: str,
                 departamento: str, cargo: str, biografia: str):
        super().__init__(id, nombre_completo, email, password, telefono, oficina)
        self._departamento = departamento
        self._cargo = cargo
        self._biografia = biografia

    @property
    def departamento(self) -> str:
        return self._departamento

    @departamento.setter
    def departamento(self, value: str):
        self._departamento = value

    @property
    def cargo(self) -> str:
        return self._cargo

    @cargo.setter
    def cargo(self, value: str):
        self._cargo = value

    @property
    def biografia(self) -> str:
        return self._biografia

    @biografia.setter
    def biografia(self, value: str):
        self._biografia = value

    def get_rol(self) -> str:
        return "Administrativo"

    def to_dict(self) -> Dict:
        return {
            'id': self._id,
            'nombre_completo': self._nombre_completo,
            'email': self._email,
            'telefono': self._telefono,
            'oficina': self._oficina,
            'departamento': self._departamento,
            'cargo': self._cargo,
            'biografia': self._biografia,
            'rol': self.get_rol(),
            'activo': self._activo
        }
