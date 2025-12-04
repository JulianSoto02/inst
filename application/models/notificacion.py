"""
Modelo de Notificación
Sistema de notificaciones para usuarios.
Aplica principio SRP.
"""

from typing import Optional, Dict
from datetime import datetime
from enum import Enum


class TipoNotificacion(Enum):
    """Tipos de notificaciones en el sistema"""
    INFO = "info"
    ADVERTENCIA = "warning"
    EXITO = "success"
    ERROR = "error"


class Notificacion:
    """Representa una notificación del sistema"""

    def __init__(self, id: Optional[int], usuario_id: int, titulo: str,
                 mensaje: str, tipo: TipoNotificacion = TipoNotificacion.INFO):
        self._id = id
        self._usuario_id = usuario_id
        self._titulo = titulo
        self._mensaje = mensaje
        self._tipo = tipo
        self._leida = False
        self._fecha_creacion = datetime.now()

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def usuario_id(self) -> int:
        return self._usuario_id

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def mensaje(self) -> str:
        return self._mensaje

    @property
    def tipo(self) -> TipoNotificacion:
        return self._tipo

    @property
    def leida(self) -> bool:
        return self._leida

    @property
    def fecha_creacion(self) -> datetime:
        return self._fecha_creacion

    def marcar_como_leida(self):
        """Marca la notificación como leída"""
        self._leida = True

    def to_dict(self) -> Dict:
        return {
            'id': self._id,
            'usuario_id': self._usuario_id,
            'titulo': self._titulo,
            'mensaje': self._mensaje,
            'tipo': self._tipo.value,
            'leida': self._leida,
            'fecha_creacion': self._fecha_creacion.isoformat()
        }

    def __str__(self) -> str:
        estado = "Leída" if self._leida else "No leída"
        return f"{self._titulo} - {estado}"
