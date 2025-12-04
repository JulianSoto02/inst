"""
Servicio Administrativo
Capa de Negocio - Lógica para gestión administrativa.
Aplica principios SOLID.
"""

from typing import List, Dict, Optional
from application.repositories.usuario_repository import UsuarioRepository
from application.repositories.materia_repository import MateriaRepository
from application.repositories.preferencia_repository import PreferenciaRepository
from application.patterns.observer import AsignacionSubject, PreferenciaSubject, NotificacionObserver
from application.repositories.notificacion_repository import NotificacionRepository
from application.models.user import Docente


class AdministrativoService:
    """Servicio para operaciones administrativas - Principio SRP"""

    def __init__(self, usuario_repo: UsuarioRepository, materia_repo: MateriaRepository,
                 preferencia_repo: PreferenciaRepository, notificacion_repo: NotificacionRepository):
        self._usuario_repo = usuario_repo
        self._materia_repo = materia_repo
        self._preferencia_repo = preferencia_repo
        self._notificacion_repo = notificacion_repo

        # Patrón Observer: Configurar sujetos y observadores
        self._asignacion_subject = AsignacionSubject()
        self._preferencia_subject = PreferenciaSubject()

        # Agregar observers
        notif_observer = NotificacionObserver(notificacion_repo)
        self._asignacion_subject.agregar_observer(notif_observer)
        self._preferencia_subject.agregar_observer(notif_observer)

    def obtener_resumen_dashboard(self) -> Dict:
        """Obtiene datos para el dashboard administrativo"""
        materias = self._materia_repo.obtener_todos()
        docentes = self._usuario_repo.obtener_docentes()

        materias_sin_asignar = [m for m in materias if m.docente_id is None]
        urgentes = len(materias_sin_asignar)

        return {
            'materias_pendientes': len(materias_sin_asignar),
            'profesores_disponibles': len(docentes),
            'urgentes_asignar': urgentes,
            'asignaturas_pendientes': materias_sin_asignar[:4]  # Primeras 4
        }

    def obtener_docentes(self) -> List[Dict]:
        """Obtiene lista de docentes con sus asignaciones"""
        docentes = self._usuario_repo.obtener_docentes()
        resultado = []

        for docente in docentes:
            materias = self._materia_repo.obtener_por_docente(docente.id)
            resultado.append({
                'id': docente.id,
                'nombre': docente.nombre_completo,
                'email': docente.email,
                'usuario': docente.email.split('@')[0],
                'clave': f"{docente.nombre_completo.split()[0].lower()}{docente.id}23",
                'materias_asignadas': len(materias),
                'estado': 'Modificado' if len(materias) > 0 else 'Pendiente'
            })

        return resultado

    def obtener_materias_sin_asignar(self) -> List[Dict]:
        """Obtiene materias que no tienen docente asignado"""
        materias = self._materia_repo.obtener_sin_asignar()
        return [m.to_dict() for m in materias]

    def asignar_materia_docente(self, materia_id: int, docente_id: Optional[int]) -> tuple[bool, str]:
        """
        Asigna o desasigna un docente a una materia.
        Usa patrón Observer para notificar al docente.
        """
        materia = self._materia_repo.obtener_por_id(materia_id)
        if not materia:
            return (False, "Materia no encontrada")

        if docente_id:
            docente = self._usuario_repo.obtener_por_id(docente_id, 'docente')
            if not docente:
                return (False, "Docente no encontrado")

        # Realizar asignación
        if self._materia_repo.asignar_docente(materia_id, docente_id):
            # Notificar usando patrón Observer
            if docente_id:
                self._asignacion_subject.crear_asignacion(
                    docente_id=docente_id,
                    materia_id=materia_id,
                    materia_nombre=materia.nombre
                )
            return (True, "Asignación realizada correctamente")

        return (False, "Error al realizar asignación")

    def obtener_preferencias_pendientes(self) -> List[Dict]:
        """Obtiene preferencias pendientes de aprobación"""
        from application.models.preferencia import EstadoPreferencia
        preferencias = self._preferencia_repo.obtener_por_estado(EstadoPreferencia.PENDIENTE)
        resultado = []

        for pref in preferencias:
            docente = self._usuario_repo.obtener_por_id(pref.docente_id, 'docente')
            materia = self._materia_repo.obtener_por_id(pref.materia_id)

            resultado.append({
                'id': pref.id,
                'docente_nombre': docente.nombre_completo if docente else 'Desconocido',
                'docente_id': pref.docente_id,
                'materia_nombre': materia.nombre if materia else 'Desconocida',
                'dia': pref.dia_semana,
                'horario': pref.horario,
                'estado': pref.estado.value
            })

        return resultado

    def aprobar_preferencia(self, preferencia_id: int) -> tuple[bool, str]:
        """
        Aprueba una preferencia.
        Usa patrón Observer para notificar al docente.
        """
        pref = self._preferencia_repo.obtener_por_id(preferencia_id)
        if not pref:
            return (False, "Preferencia no encontrada")

        if self._preferencia_repo.aprobar_preferencia(preferencia_id):
            # Notificar usando patrón Observer
            materia = self._materia_repo.obtener_por_id(pref.materia_id)
            self._preferencia_subject.aprobar_preferencia(
                docente_id=pref.docente_id,
                materia_nombre=materia.nombre if materia else 'Desconocida'
            )
            return (True, "Preferencia aprobada")

        return (False, "Error al aprobar preferencia")

    def rechazar_preferencia(self, preferencia_id: int) -> tuple[bool, str]:
        """
        Rechaza una preferencia.
        Usa patrón Observer para notificar al docente.
        """
        pref = self._preferencia_repo.obtener_por_id(preferencia_id)
        if not pref:
            return (False, "Preferencia no encontrada")

        if self._preferencia_repo.rechazar_preferencia(preferencia_id):
            # Notificar usando patrón Observer
            materia = self._materia_repo.obtener_por_id(pref.materia_id)
            self._preferencia_subject.rechazar_preferencia(
                docente_id=pref.docente_id,
                materia_nombre=materia.nombre if materia else 'Desconocida'
            )
            return (True, "Preferencia rechazada")

        return (False, "Error al rechazar preferencia")

    def crear_docente(self, datos: Dict) -> tuple[bool, str]:
        """Crea un nuevo docente en el sistema"""
        from application.patterns.factory import UsuarioFactory

        try:
            docente = UsuarioFactory.crear_usuario('docente', datos)
            self._usuario_repo.crear(docente)
            return (True, "Docente creado correctamente")
        except Exception as e:
            return (False, f"Error al crear docente: {str(e)}")

    def actualizar_docente(self, docente: Docente) -> tuple[bool, str]:
        """Actualiza información de un docente"""
        if self._usuario_repo.actualizar(docente):
            return (True, "Docente actualizado correctamente")
        return (False, "Error al actualizar docente")

    def obtener_notificaciones_no_leidas(self, usuario_id: int) -> int:
        """Obtiene el conteo de notificaciones no leídas"""
        notificaciones = self._notificacion_repo.obtener_no_leidas(usuario_id)
        return len(notificaciones)
