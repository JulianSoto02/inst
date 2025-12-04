"""
Modelo de Preferencia de Enseñanza
Permite a los docentes registrar sus preferencias de horario y materias.
"""

from typing import Optional, Dict
from enum import Enum


class EstadoPreferencia(Enum):
    """Estados posibles de una preferencia"""
    PENDIENTE = "Pendiente"
    APROBADA = "Aprobada"
    RECHAZADA = "Rechazada"


class PreferenciaEnsenanza:
    """Representa una preferencia de horario y materia de un docente"""

    def __init__(self, id: Optional[int], docente_id: int, materia_id: int,
                 dia_semana: str, horario: str,
                 estado: EstadoPreferencia = EstadoPreferencia.PENDIENTE):
        self._id = id
        self._docente_id = docente_id
        self._materia_id = materia_id
        self._dia_semana = dia_semana
        self._horario = horario
        self._estado = estado

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def docente_id(self) -> int:
        return self._docente_id

    @property
    def materia_id(self) -> int:
        return self._materia_id

    @materia_id.setter
    def materia_id(self, value: int):
        self._materia_id = value

    @property
    def dia_semana(self) -> str:
        return self._dia_semana

    @dia_semana.setter
    def dia_semana(self, value: str):
        self._dia_semana = value

    @property
    def horario(self) -> str:
        return self._horario

    @horario.setter
    def horario(self, value: str):
        self._horario = value

    @property
    def estado(self) -> EstadoPreferencia:
        return self._estado

    @estado.setter
    def estado(self, value: EstadoPreferencia):
        self._estado = value

    def aprobar(self):
        """Aprueba la preferencia"""
        self._estado = EstadoPreferencia.APROBADA

    def rechazar(self):
        """Rechaza la preferencia"""
        self._estado = EstadoPreferencia.RECHAZADA

    def to_dict(self) -> Dict:
        return {
            'id': self._id,
            'docente_id': self._docente_id,
            'materia_id': self._materia_id,
            'dia_semana': self._dia_semana,
            'horario': self._horario,
            'estado': self._estado.value
        }

    def __str__(self) -> str:
        return f"Preferencia: {self._dia_semana} {self._horario} - {self._estado.value}"
