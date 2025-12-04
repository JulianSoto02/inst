"""
Repositorio de Preferencias
Gestiona las preferencias de enseñanza de los docentes.
"""

from typing import List, Optional
from app.patterns.repository import BaseRepository
from app.models.preferencia import PreferenciaEnsenanza, EstadoPreferencia


class PreferenciaRepository(BaseRepository[PreferenciaEnsenanza]):
    """Repositorio para gestionar preferencias de enseñanza"""

    def _get_table_name(self) -> str:
        return "preferencias"

    def _map_to_entity(self, row) -> PreferenciaEnsenanza:
        estado = EstadoPreferencia(row[5]) if row[5] else EstadoPreferencia.PENDIENTE
        return PreferenciaEnsenanza(
            id=row[0],
            docente_id=row[1],
            materia_id=row[2],
            dia_semana=row[3],
            horario=row[4],
            estado=estado
        )

    def crear(self, preferencia: PreferenciaEnsenanza) -> PreferenciaEnsenanza:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO preferencias (docente_id, materia_id, dia_semana, horario, estado)
            VALUES (?, ?, ?, ?, ?)
        """, (preferencia.docente_id, preferencia.materia_id, preferencia.dia_semana,
              preferencia.horario, preferencia.estado.value))
        conn.commit()
        preferencia.id = cursor.lastrowid
        return preferencia

    def actualizar(self, preferencia: PreferenciaEnsenanza) -> bool:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE preferencias
            SET materia_id = ?, dia_semana = ?, horario = ?, estado = ?
            WHERE id = ?
        """, (preferencia.materia_id, preferencia.dia_semana, preferencia.horario,
              preferencia.estado.value, preferencia.id))
        conn.commit()
        return cursor.rowcount > 0

    def eliminar(self, id: int) -> bool:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM preferencias WHERE id = ?", (id,))
        conn.commit()
        return cursor.rowcount > 0

    def obtener_por_docente(self, docente_id: int) -> List[PreferenciaEnsenanza]:
        """Obtiene todas las preferencias de un docente"""
        cursor = self._db.get_connection().cursor()
        cursor.execute("SELECT * FROM preferencias WHERE docente_id = ?", (docente_id,))
        return [self._map_to_entity(row) for row in cursor.fetchall()]

    def obtener_por_estado(self, estado: EstadoPreferencia) -> List[PreferenciaEnsenanza]:
        """Obtiene preferencias por estado"""
        cursor = self._db.get_connection().cursor()
        cursor.execute("SELECT * FROM preferencias WHERE estado = ?", (estado.value,))
        return [self._map_to_entity(row) for row in cursor.fetchall()]

    def aprobar_preferencia(self, id: int) -> bool:
        """Aprueba una preferencia"""
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE preferencias SET estado = ? WHERE id = ?",
                      (EstadoPreferencia.APROBADA.value, id))
        conn.commit()
        return cursor.rowcount > 0

    def rechazar_preferencia(self, id: int) -> bool:
        """Rechaza una preferencia"""
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE preferencias SET estado = ? WHERE id = ?",
                      (EstadoPreferencia.RECHAZADA.value, id))
        conn.commit()
        return cursor.rowcount > 0
