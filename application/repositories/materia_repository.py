"""
Repositorio de Materias
Implementa patrón Repository para materias y horarios.
"""

from typing import List, Optional
from application.patterns.repository import BaseRepository
from application.models.materia import Materia, HorarioClase


class MateriaRepository(BaseRepository[Materia]):
    """Repositorio para gestionar materias"""

    def _get_table_name(self) -> str:
        return "materias"

    def _map_to_entity(self, row) -> Materia:
        return Materia(
            id=row[0],
            nombre=row[1],
            codigo=row[2],
            aula=row[3],
            creditos=row[4],
            descripcion=row[5] or ""
        )

    def crear(self, materia: Materia) -> Materia:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO materias (nombre, codigo, aula, creditos, descripcion, docente_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (materia.nombre, materia.codigo, materia.aula, materia.creditos,
              materia.descripcion, materia.docente_id))
        conn.commit()
        materia.id = cursor.lastrowid
        return materia

    def actualizar(self, materia: Materia) -> bool:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE materias
            SET nombre = ?, codigo = ?, aula = ?, creditos = ?, descripcion = ?, docente_id = ?
            WHERE id = ?
        """, (materia.nombre, materia.codigo, materia.aula, materia.creditos,
              materia.descripcion, materia.docente_id, materia.id))
        conn.commit()
        return cursor.rowcount > 0

    def eliminar(self, id: int) -> bool:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM materias WHERE id = ?", (id,))
        conn.commit()
        return cursor.rowcount > 0

    def asignar_docente(self, materia_id: int, docente_id: Optional[int]) -> bool:
        """Asigna o desasigna un docente a una materia"""
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE materias SET docente_id = ? WHERE id = ?",
                      (docente_id, materia_id))
        conn.commit()
        return cursor.rowcount > 0

    def obtener_por_docente(self, docente_id: int) -> List[Materia]:
        """Obtiene todas las materias asignadas a un docente"""
        cursor = self._db.get_connection().cursor()
        cursor.execute("SELECT * FROM materias WHERE docente_id = ?", (docente_id,))
        return [self._map_to_entity(row) for row in cursor.fetchall()]

    def obtener_sin_asignar(self) -> List[Materia]:
        """Obtiene materias sin docente asignado"""
        cursor = self._db.get_connection().cursor()
        cursor.execute("SELECT * FROM materias WHERE docente_id IS NULL")
        return [self._map_to_entity(row) for row in cursor.fetchall()]


class HorarioRepository(BaseRepository[HorarioClase]):
    """Repositorio para gestionar horarios de clases"""

    def _get_table_name(self) -> str:
        return "horarios"

    def _map_to_entity(self, row) -> HorarioClase:
        return HorarioClase(
            id=row[0],
            materia_id=row[1],
            dia_semana=row[2],
            hora_inicio=row[3],
            hora_fin=row[4]
        )

    def crear(self, horario: HorarioClase) -> HorarioClase:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO horarios (materia_id, dia_semana, hora_inicio, hora_fin)
            VALUES (?, ?, ?, ?)
        """, (horario.materia_id, horario.dia_semana, horario.hora_inicio, horario.hora_fin))
        conn.commit()
        horario.id = cursor.lastrowid
        return horario

    def actualizar(self, horario: HorarioClase) -> bool:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE horarios
            SET dia_semana = ?, hora_inicio = ?, hora_fin = ?
            WHERE id = ?
        """, (horario.dia_semana, horario.hora_inicio, horario.hora_fin, horario.id))
        conn.commit()
        return cursor.rowcount > 0

    def eliminar(self, id: int) -> bool:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM horarios WHERE id = ?", (id,))
        conn.commit()
        return cursor.rowcount > 0

    def obtener_por_materia(self, materia_id: int) -> List[HorarioClase]:
        """Obtiene todos los horarios de una materia"""
        cursor = self._db.get_connection().cursor()
        cursor.execute("SELECT * FROM horarios WHERE materia_id = ?", (materia_id,))
        return [self._map_to_entity(row) for row in cursor.fetchall()]

    def obtener_por_dia(self, dia_semana: str) -> List[HorarioClase]:
        """Obtiene todos los horarios de un día específico"""
        cursor = self._db.get_connection().cursor()
        cursor.execute("SELECT * FROM horarios WHERE dia_semana = ?", (dia_semana,))
        return [self._map_to_entity(row) for row in cursor.fetchall()]
