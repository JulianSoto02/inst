"""
Modelo de Materia - Capa de Datos
Representa las materias/asignaturas del sistema universitario.
Aplica principio SRP: Una única responsabilidad.
"""

from typing import Optional, Dict
from datetime import time


class Materia:
    """Representa una materia/asignatura en el sistema"""

    def __init__(self, id: Optional[int], nombre: str, codigo: str,
                 aula: str, creditos: int = 3, descripcion: str = ""):
        self._id = id
        self._nombre = nombre
        self._codigo = codigo
        self._aula = aula
        self._creditos = creditos
        self._descripcion = descripcion
        self._docente_id: Optional[int] = None

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str):
        self._nombre = value

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, value: str):
        self._codigo = value

    @property
    def aula(self) -> str:
        return self._aula

    @aula.setter
    def aula(self, value: str):
        self._aula = value

    @property
    def creditos(self) -> int:
        return self._creditos

    @creditos.setter
    def creditos(self, value: int):
        self._creditos = value

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, value: str):
        self._descripcion = value

    @property
    def docente_id(self) -> Optional[int]:
        return self._docente_id

    @docente_id.setter
    def docente_id(self, value: Optional[int]):
        self._docente_id = value

    def to_dict(self) -> Dict:
        return {
            'id': self._id,
            'nombre': self._nombre,
            'codigo': self._codigo,
            'aula': self._aula,
            'creditos': self._creditos,
            'descripcion': self._descripcion,
            'docente_id': self._docente_id
        }

    def __str__(self) -> str:
        return f"{self._nombre} ({self._codigo}) - Aula {self._aula}"


class HorarioClase:
    """Representa un horario específico de clase"""

    DIAS_SEMANA = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']

    def __init__(self, id: Optional[int], materia_id: int,
                 dia_semana: str, hora_inicio: str, hora_fin: str):
        self._id = id
        self._materia_id = materia_id
        self._dia_semana = dia_semana
        self._hora_inicio = hora_inicio
        self._hora_fin = hora_fin

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def materia_id(self) -> int:
        return self._materia_id

    @property
    def dia_semana(self) -> str:
        return self._dia_semana

    @dia_semana.setter
    def dia_semana(self, value: str):
        if value not in self.DIAS_SEMANA:
            raise ValueError(f"Día inválido. Debe ser uno de: {', '.join(self.DIAS_SEMANA)}")
        self._dia_semana = value

    @property
    def hora_inicio(self) -> str:
        return self._hora_inicio

    @hora_inicio.setter
    def hora_inicio(self, value: str):
        self._hora_inicio = value

    @property
    def hora_fin(self) -> str:
        return self._hora_fin

    @hora_fin.setter
    def hora_fin(self, value: str):
        self._hora_fin = value

    def to_dict(self) -> Dict:
        return {
            'id': self._id,
            'materia_id': self._materia_id,
            'dia_semana': self._dia_semana,
            'hora_inicio': self._hora_inicio,
            'hora_fin': self._hora_fin
        }

    def __str__(self) -> str:
        return f"{self._dia_semana} {self._hora_inicio} - {self._hora_fin}"
