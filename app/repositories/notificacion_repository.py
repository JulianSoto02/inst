"""
Repositorio de Notificaciones
Gestiona las notificaciones del sistema.
"""

from typing import List, Optional
from app.patterns.repository import BaseRepository
from app.models.notificacion import Notificacion, TipoNotificacion
from datetime import datetime


class NotificacionRepository(BaseRepository[Notificacion]):
    """Repositorio para gestionar notificaciones"""

    def _get_table_name(self) -> str:
        return "notificaciones"

    def _map_to_entity(self, row) -> Notificacion:
        notif = Notificacion(
            id=row[0],
            usuario_id=row[1],
            titulo=row[2],
            mensaje=row[3],
            tipo=TipoNotificacion(row[4])
        )
        notif._leida = bool(row[5])
        notif._fecha_creacion = datetime.fromisoformat(row[6]) if row[6] else datetime.now()
        return notif

    def crear(self, notificacion: Notificacion) -> Notificacion:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO notificaciones (usuario_id, titulo, mensaje, tipo, leida, fecha_creacion)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (notificacion.usuario_id, notificacion.titulo, notificacion.mensaje,
              notificacion.tipo.value, 0, notificacion.fecha_creacion.isoformat()))
        conn.commit()
        notificacion.id = cursor.lastrowid
        return notificacion

    def actualizar(self, notificacion: Notificacion) -> bool:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE notificaciones SET leida = ? WHERE id = ?
        """, (1 if notificacion.leida else 0, notificacion.id))
        conn.commit()
        return cursor.rowcount > 0

    def eliminar(self, id: int) -> bool:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notificaciones WHERE id = ?", (id,))
        conn.commit()
        return cursor.rowcount > 0

    def obtener_por_usuario(self, usuario_id: int) -> List[Notificacion]:
        """Obtiene todas las notificaciones de un usuario"""
        cursor = self._db.get_connection().cursor()
        cursor.execute("""
            SELECT * FROM notificaciones WHERE usuario_id = ? ORDER BY fecha_creacion DESC
        """, (usuario_id,))
        return [self._map_to_entity(row) for row in cursor.fetchall()]

    def obtener_no_leidas(self, usuario_id: int) -> List[Notificacion]:
        """Obtiene notificaciones no leídas de un usuario"""
        cursor = self._db.get_connection().cursor()
        cursor.execute("""
            SELECT * FROM notificaciones
            WHERE usuario_id = ? AND leida = 0
            ORDER BY fecha_creacion DESC
        """, (usuario_id,))
        return [self._map_to_entity(row) for row in cursor.fetchall()]

    def marcar_como_leida(self, id: int) -> bool:
        """Marca una notificación como leída"""
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE notificaciones SET leida = 1 WHERE id = ?", (id,))
        conn.commit()
        return cursor.rowcount > 0

    def marcar_todas_leidas(self, usuario_id: int) -> bool:
        """Marca todas las notificaciones de un usuario como leídas"""
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE notificaciones SET leida = 1 WHERE usuario_id = ?",
                      (usuario_id,))
        conn.commit()
        return cursor.rowcount > 0
