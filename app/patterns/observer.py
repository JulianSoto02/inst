"""
PATRÓN OBSERVER (Comportamiento)
================================
Define una dependencia uno-a-muchos entre objetos para que cuando un objeto cambie
su estado, todos sus dependientes sean notificados automáticamente.

Ventajas:
- Bajo acoplamiento entre sujeto y observadores
- Permite agregar/eliminar observadores dinámicamente
- Notificaciones automáticas de cambios de estado

Uso en el sistema:
- Sistema de notificaciones para usuarios
- Notificar cambios en asignaciones de materias
- Alertas de cambios en preferencias
"""

from abc import ABC, abstractmethod
from typing import List, Dict
from app.models.notificacion import Notificacion, TipoNotificacion


class Observer(ABC):
    """
    Interfaz Observer - Observador abstracto.
    Principio ISP: Interfaz específica y segregada.
    """

    @abstractmethod
    def actualizar(self, evento: str, datos: Dict):
        """
        Método llamado cuando el sujeto notifica un cambio.

        Args:
            evento: Tipo de evento que ocurrió
            datos: Datos relacionados con el evento
        """
        pass


class Subject(ABC):
    """
    Interfaz Subject - Sujeto observable abstracto.
    Principio OCP: Abierto para extensión.
    """

    def __init__(self):
        self._observers: List[Observer] = []

    def agregar_observer(self, observer: Observer):
        """Agrega un observador a la lista"""
        if observer not in self._observers:
            self._observers.append(observer)

    def eliminar_observer(self, observer: Observer):
        """Elimina un observador de la lista"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notificar_observers(self, evento: str, datos: Dict):
        """Notifica a todos los observadores sobre un evento"""
        for observer in self._observers:
            observer.actualizar(evento, datos)


class NotificacionObserver(Observer):
    """
    Observer concreto que maneja notificaciones.
    Se encarga de crear notificaciones cuando ocurren eventos.

    Principio SRP: Única responsabilidad de manejar notificaciones.
    """

    def __init__(self, notificacion_repository):
        """
        Args:
            notificacion_repository: Repositorio para persistir notificaciones
        """
        self._notificacion_repository = notificacion_repository

    def actualizar(self, evento: str, datos: Dict):
        """
        Procesa eventos y crea notificaciones apropiadas.

        Args:
            evento: Tipo de evento
            datos: Datos del evento
        """
        if evento == "asignacion_creada":
            self._notificar_asignacion_creada(datos)
        elif evento == "asignacion_modificada":
            self._notificar_asignacion_modificada(datos)
        elif evento == "preferencia_aprobada":
            self._notificar_preferencia_aprobada(datos)
        elif evento == "preferencia_rechazada":
            self._notificar_preferencia_rechazada(datos)

    def _notificar_asignacion_creada(self, datos: Dict):
        """Crea notificación de nueva asignación"""
        notificacion = Notificacion(
            id=None,
            usuario_id=datos['docente_id'],
            titulo="Nueva Asignación de Materia",
            mensaje=f"Se te ha asignado la materia: {datos['materia_nombre']}",
            tipo=TipoNotificacion.EXITO
        )
        self._notificacion_repository.crear(notificacion)

    def _notificar_asignacion_modificada(self, datos: Dict):
        """Crea notificación de modificación de asignación"""
        notificacion = Notificacion(
            id=None,
            usuario_id=datos['docente_id'],
            titulo="Asignación Modificada",
            mensaje=f"Tu asignación de {datos['materia_nombre']} ha sido modificada",
            tipo=TipoNotificacion.INFO
        )
        self._notificacion_repository.crear(notificacion)

    def _notificar_preferencia_aprobada(self, datos: Dict):
        """Crea notificación de preferencia aprobada"""
        notificacion = Notificacion(
            id=None,
            usuario_id=datos['docente_id'],
            titulo="Preferencia Aprobada",
            mensaje=f"Tu preferencia para {datos['materia_nombre']} ha sido aprobada",
            tipo=TipoNotificacion.EXITO
        )
        self._notificacion_repository.crear(notificacion)

    def _notificar_preferencia_rechazada(self, datos: Dict):
        """Crea notificación de preferencia rechazada"""
        notificacion = Notificacion(
            id=None,
            usuario_id=datos['docente_id'],
            titulo="Preferencia Rechazada",
            mensaje=f"Tu preferencia para {datos['materia_nombre']} ha sido rechazada",
            tipo=TipoNotificacion.ADVERTENCIA
        )
        self._notificacion_repository.crear(notificacion)


class LogObserver(Observer):
    """
    Observer concreto que registra eventos en logs.

    Principio SRP: Única responsabilidad de logging.
    """

    def actualizar(self, evento: str, datos: Dict):
        """Registra el evento en el log"""
        print(f"[LOG] Evento: {evento} | Datos: {datos}")


class AsignacionSubject(Subject):
    """
    Sujeto concreto que maneja asignaciones de materias.
    Notifica a los observers cuando cambian las asignaciones.

    Principio SRP: Responsabilidad de gestionar y notificar asignaciones.
    """

    def crear_asignacion(self, docente_id: int, materia_id: int, materia_nombre: str):
        """
        Crea una nueva asignación y notifica a los observers.

        Args:
            docente_id: ID del docente
            materia_id: ID de la materia
            materia_nombre: Nombre de la materia
        """
        # Lógica de creación de asignación
        datos = {
            'docente_id': docente_id,
            'materia_id': materia_id,
            'materia_nombre': materia_nombre
        }

        # Notificar a todos los observers
        self.notificar_observers("asignacion_creada", datos)

    def modificar_asignacion(self, docente_id: int, materia_id: int, materia_nombre: str):
        """
        Modifica una asignación existente y notifica a los observers.

        Args:
            docente_id: ID del docente
            materia_id: ID de la materia
            materia_nombre: Nombre de la materia
        """
        datos = {
            'docente_id': docente_id,
            'materia_id': materia_id,
            'materia_nombre': materia_nombre
        }

        # Notificar a todos los observers
        self.notificar_observers("asignacion_modificada", datos)


class PreferenciaSubject(Subject):
    """
    Sujeto concreto que maneja preferencias de enseñanza.
    Notifica cuando se aprueban o rechazan preferencias.
    """

    def aprobar_preferencia(self, docente_id: int, materia_nombre: str):
        """
        Aprueba una preferencia y notifica.

        Args:
            docente_id: ID del docente
            materia_nombre: Nombre de la materia
        """
        datos = {
            'docente_id': docente_id,
            'materia_nombre': materia_nombre
        }
        self.notificar_observers("preferencia_aprobada", datos)

    def rechazar_preferencia(self, docente_id: int, materia_nombre: str):
        """
        Rechaza una preferencia y notifica.

        Args:
            docente_id: ID del docente
            materia_nombre: Nombre de la materia
        """
        datos = {
            'docente_id': docente_id,
            'materia_nombre': materia_nombre
        }
        self.notificar_observers("preferencia_rechazada", datos)


# Ejemplo de uso:
"""
# Crear repositorio de notificaciones
from app.repositories.notificacion_repository import NotificacionRepository
notif_repo = NotificacionRepository()

# Crear observers
notif_observer = NotificacionObserver(notif_repo)
log_observer = LogObserver()

# Crear sujeto y agregar observers
asignacion_subject = AsignacionSubject()
asignacion_subject.agregar_observer(notif_observer)
asignacion_subject.agregar_observer(log_observer)

# Cuando se crea una asignación, todos los observers son notificados
asignacion_subject.crear_asignacion(
    docente_id=1,
    materia_id=5,
    materia_nombre="Cálculo Diferencial"
)
# Esto creará automáticamente:
# 1. Una notificación en la base de datos (NotificacionObserver)
# 2. Un registro en el log (LogObserver)
"""
