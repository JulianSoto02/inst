"""
Script de Inicialización de Base de Datos
Crea todas las tablas necesarias para el sistema universitario.
"""

import sqlite3
import os


def crear_base_datos():
    """Crea la base de datos y todas las tablas"""

    # Ruta de la base de datos
    db_path = os.path.join(os.path.dirname(__file__), 'universidad.db')

    # Eliminar BD existente si existe
    if os.path.exists(db_path):
        os.remove(db_path)
        print("✓ Base de datos anterior eliminada")

    # Crear conexión
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Creando tablas...")

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
    print("✓ Tabla 'docentes' creada")

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
    print("✓ Tabla 'administrativos' creada")

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
    print("✓ Tabla 'materias' creada")

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
    print("✓ Tabla 'horarios' creada")

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
    print("✓ Tabla 'preferencias' creada")

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
    print("✓ Tabla 'notificaciones' creada")

    # Crear índices para mejorar rendimiento
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_materias_docente ON materias(docente_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_horarios_materia ON horarios(materia_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_preferencias_docente ON preferencias(docente_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_notificaciones_usuario ON notificaciones(usuario_id)")
    print("✓ Índices creados")

    conn.commit()
    conn.close()

    print(f"\n✓ Base de datos creada exitosamente en: {db_path}")
    return db_path


if __name__ == "__main__":
    crear_base_datos()
