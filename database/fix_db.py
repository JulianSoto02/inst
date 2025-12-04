"""
Script para reparar/crear tablas de Base de Datos
Crea las tablas sin eliminar la base de datos existente.
"""

import sqlite3
import os


def reparar_base_datos():
    """Crea las tablas si no existen"""

    # Ruta de la base de datos
    db_path = os.path.join(os.path.dirname(__file__), 'universidad.db')

    # Crear conexión
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Creando/verificando tablas...")

    # Tabla de Docentes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS docentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_completo TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            telefono TEXT,
            oficina TEXT,
            departamento TEXT,
            especialidad TEXT,
            biografia TEXT,
            activo INTEGER DEFAULT 1,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("[OK] Tabla 'docentes' verificada")

    # Tabla de Administrativos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS administrativos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_completo TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            telefono TEXT,
            oficina TEXT,
            departamento TEXT,
            cargo TEXT,
            biografia TEXT,
            activo INTEGER DEFAULT 1,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("[OK] Tabla 'administrativos' verificada")

    # Tabla de Materias
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS materias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            codigo TEXT UNIQUE NOT NULL,
            aula TEXT NOT NULL,
            creditos INTEGER DEFAULT 3,
            descripcion TEXT,
            docente_id INTEGER,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (docente_id) REFERENCES docentes(id)
        )
    """)
    print("[OK] Tabla 'materias' verificada")

    # Tabla de Horarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS horarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            materia_id INTEGER NOT NULL,
            dia_semana TEXT NOT NULL,
            hora_inicio TEXT NOT NULL,
            hora_fin TEXT NOT NULL,
            FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE
        )
    """)
    print("[OK] Tabla 'horarios' verificada")

    # Tabla de Preferencias
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS preferencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            docente_id INTEGER NOT NULL,
            materia_id INTEGER NOT NULL,
            dia_semana TEXT NOT NULL,
            horario TEXT NOT NULL,
            estado TEXT DEFAULT 'Pendiente',
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (docente_id) REFERENCES docentes(id),
            FOREIGN KEY (materia_id) REFERENCES materias(id)
        )
    """)
    print("[OK] Tabla 'preferencias' verificada")

    # Tabla de Notificaciones
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notificaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            mensaje TEXT NOT NULL,
            tipo TEXT DEFAULT 'info',
            leida INTEGER DEFAULT 0,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("[OK] Tabla 'notificaciones' verificada")

    # Crear índices para mejorar rendimiento
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_materias_docente ON materias(docente_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_horarios_materia ON horarios(materia_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_preferencias_docente ON preferencias(docente_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_notificaciones_usuario ON notificaciones(usuario_id)")
    print("[OK] Indices verificados")

    conn.commit()
    conn.close()

    print(f"\n[OK] Base de datos reparada exitosamente: {db_path}")
    return db_path


if __name__ == "__main__":
    reparar_base_datos()
