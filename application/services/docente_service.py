"""
Servicio de Docente
Capa de Negocio - Lógica relacionada con docentes.
Aplica principios SOLID.
"""

from typing import List, Dict, Optional
from application.repositories.usuario_repository import UsuarioRepository
from application.repositories.materia_repository import MateriaRepository, HorarioRepository
from application.repositories.preferencia_repository import PreferenciaRepository
from application.repositories.notificacion_repository import NotificacionRepository
from application.models.user import Docente
from application.models.materia import Materia
from application.models.preferencia import PreferenciaEnsenanza, EstadoPreferencia


class DocenteService:
    """Servicio para operaciones de docentes - Principio SRP"""

    def __init__(self, usuario_repo: UsuarioRepository, materia_repo: MateriaRepository,
                 preferencia_repo: PreferenciaRepository, horario_repo: HorarioRepository,
                 notificacion_repo: NotificacionRepository):
        self._usuario_repo = usuario_repo
        self._materia_repo = materia_repo
        self._preferencia_repo = preferencia_repo
        self._horario_repo = horario_repo
        self._notificacion_repo = notificacion_repo

    def obtener_perfil(self, docente_id: int) -> Optional[Docente]:
        """Obtiene el perfil completo del docente"""
        return self._usuario_repo.obtener_por_id(docente_id, 'docente')

    def actualizar_perfil(self, docente: Docente) -> tuple[bool, str]:
        """Actualiza el perfil del docente"""
        if self._usuario_repo.actualizar(docente):
            return (True, "Perfil actualizado correctamente")
        return (False, "Error al actualizar perfil")

    def obtener_materias_asignadas(self, docente_id: int) -> List[Materia]:
        """Obtiene las materias asignadas al docente"""
        return self._materia_repo.obtener_por_docente(docente_id)

    def obtener_resumen_dashboard(self, docente_id: int) -> Dict:
        """Obtiene datos para el dashboard del docente"""
        materias = self.obtener_materias_asignadas(docente_id)
        preferencias = self._preferencia_repo.obtener_por_docente(docente_id)

        # Calcular horas semanales
        horas_totales = 0
        for materia in materias:
            horarios = self._horario_repo.obtener_por_materia(materia.id)
            for horario in horarios:
                # Calcular horas (simplificado)
                horas_totales += 2  # Asumimos 2 horas por sesión

        # Preferencias pendientes
        preferencias_pendientes = [p for p in preferencias if p.estado == EstadoPreferencia.PENDIENTE]

        # Próximas clases (simplificado - obtener las de esta semana)
        proximas_clases = []
        for materia in materias[:4]:  # Primeras 4
            horarios = self._horario_repo.obtener_por_materia(materia.id)
            if horarios:
                proximas_clases.append({
                    'materia': materia.nombre,
                    'aula': materia.aula,
                    'dia': horarios[0].dia_semana,
                    'horario': f"{horarios[0].hora_inicio} - {horarios[0].hora_fin}"
                })

        return {
            'materias_asignadas': len(materias),
            'horas_semanales': horas_totales,
            'proximas_clases': len(materias),
            'preferencias_pendientes': len(preferencias_pendientes),
            'lista_proximas_clases': proximas_clases
        }

    def obtener_horario_semanal(self, docente_id: int) -> Dict:
        """Obtiene el horario semanal completo del docente"""
        materias = self.obtener_materias_asignadas(docente_id)

        horario_por_dia = {
            'Lunes': [],
            'Martes': [],
            'Miércoles': [],
            'Jueves': [],
            'Viernes': [],
            'Sábado': []
        }

        for materia in materias:
            horarios = self._horario_repo.obtener_por_materia(materia.id)
            for horario in horarios:
                if horario.dia_semana in horario_por_dia:
                    horario_por_dia[horario.dia_semana].append({
                        'materia': materia.nombre,
                        'aula': materia.aula,
                        'hora_inicio': horario.hora_inicio,
                        'hora_fin': horario.hora_fin
                    })

        # Calcular estadísticas
        total_horas = sum(len(clases) * 2 for clases in horario_por_dia.values())
        clases_por_semana = sum(len(clases) for clases in horario_por_dia.values())

        return {
            'horario_por_dia': horario_por_dia,
            'total_horas': total_horas,
            'clases_por_semana': clases_por_semana,
            'materias_diferentes': len(materias)
        }

    def obtener_preferencias(self, docente_id: int) -> List[Dict]:
        """Obtiene las preferencias del docente con información adicional"""
        preferencias = self._preferencia_repo.obtener_por_docente(docente_id)
        resultado = []

        for pref in preferencias:
            materia = self._materia_repo.obtener_por_id(pref.materia_id)
            resultado.append({
                'id': pref.id,
                'materia': materia.nombre if materia else 'Desconocida',
                'dia': pref.dia_semana,
                'horario': pref.horario,
                'estado': pref.estado.value
            })

        return resultado

    def crear_preferencia(self, docente_id: int, materia_id: int,
                         dia_semana: str, horario: str) -> tuple[bool, str]:
        """Crea una nueva preferencia de enseñanza"""
        preferencia = PreferenciaEnsenanza(
            id=None,
            docente_id=docente_id,
            materia_id=materia_id,
            dia_semana=dia_semana,
            horario=horario,
            estado=EstadoPreferencia.PENDIENTE
        )

        try:
            self._preferencia_repo.crear(preferencia)
            return (True, "Preferencia creada correctamente")
        except Exception as e:
            return (False, f"Error al crear preferencia: {str(e)}")

    def obtener_notificaciones(self, docente_id: int) -> List[Dict]:
        """Obtiene las notificaciones del docente"""
        notificaciones = self._notificacion_repo.obtener_por_usuario(docente_id)
        return [n.to_dict() for n in notificaciones]

    def obtener_notificaciones_no_leidas(self, docente_id: int) -> int:
        """Obtiene el conteo de notificaciones no leídas"""
        notificaciones = self._notificacion_repo.obtener_no_leidas(docente_id)
        return len(notificaciones)

    def marcar_notificacion_leida(self, notificacion_id: int) -> bool:
        """Marca una notificación como leída"""
        return self._notificacion_repo.marcar_como_leida(notificacion_id)
