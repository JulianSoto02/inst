"""
Script para poblar la base de datos con datos de prueba.
Crea usuarios, materias y horarios de ejemplo.
"""

import sqlite3
import hashlib
import os


def hash_password(password: str) -> str:
    """Genera hash SHA-256 de contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()


def poblar_datos():
    """Inserta datos de prueba en la base de datos"""

    db_path = os.path.join(os.path.dirname(__file__), 'universidad.db')

    if not os.path.exists(db_path):
        print("Error: La base de datos no existe. Ejecuta init_db.py primero.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Insertando datos de prueba...")

    # Insertar Docentes
    docentes = [
        ('Dr. Carlos Martínez', 'docente@demo.com', 'docente123', '+52 555 123 4567',
         'Edificio A - Oficina 12', 'Matemáticas', 'Cálculo y Análisis Matemático',
         'Doctor en Matemáticas con 15 años de experiencia en docencia universitaria. Especializado en cálculo diferencial e integral.'),

        ('Tatiana Cabrera', 'taticabrera@docente.demo.edu.co', 'Tatica2910',
         '+52 555 234 5678', 'Edificio B - Oficina 05', 'Matemáticas', 'Álgebra',
         'Maestra en Álgebra con experiencia en educación superior.'),

        ('José Castro', 'joseca@docente.demo.edu.co', 'Josec@23', '+52 555 345 6789',
         'Edificio A - Oficina 08', 'Matemáticas', 'Estadística',
         'Especialista en estadística aplicada y probabilidad.'),

        ('Ángela Robles', 'angel4o@docente.demo.edu.co', 'angel3291', '+52 555 456 7890',
         'Edificio C - Oficina 10', 'Matemáticas', 'Geometría',
         'Doctora en Geometría Analítica.'),

        ('Juan Camilo Bohorquez', 'juancabohor@docente.demo.edu.co', 'juanca29012',
         '+52 555 567 8901', 'Edificio B - Oficina 15', 'Matemáticas', 'Cálculo Integral',
         'Experto en cálculo integral y ecuaciones diferenciales.'),

        ('Diana Montoya', 'dianamont@docente.demo.coo', 'infinto2301', '+52 555 678 9012',
         'Edificio A - Oficina 20', 'Matemáticas', 'Probabilidad',
         'Especialista en teoría de probabilidades.'),
    ]

    for docente in docentes:
        cursor.execute("""
            INSERT INTO docentes (nombre_completo, email, password, telefono, oficina,
                                departamento, especialidad, biografia)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (docente[0], docente[1], hash_password(docente[2]), docente[3],
              docente[4], docente[5], docente[6], docente[7]))

    print(f"[OK] {len(docentes)} docentes insertados")

    # Insertar Administrativos
    administrativos = [
        ('David Piedrahita', 'administrativo@demo.com', 'admin123', '+52 525 876 3597',
         'Edificio A - Oficina 12', 'Administrativo', 'Encargado de asignaciones',
         'Profesional en Administración de empresas con especialización en gestión educativa y experiencia en planeación académica universitaria.')
    ]

    for admin in administrativos:
        cursor.execute("""
            INSERT INTO administrativos (nombre_completo, email, password, telefono, oficina,
                                        departamento, cargo, biografia)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (admin[0], admin[1], hash_password(admin[2]), admin[3],
              admin[4], admin[5], admin[6], admin[7]))

    print(f"[OK] {len(administrativos)} administrativos insertados")

    # Insertar Materias
    materias = [
        ('Cálculo Diferencial', 'MAT101', 'Aula 301', 4, 'Introducción al cálculo diferencial'),
        ('Álgebra Lineal', 'MAT102', 'Aula 205', 4, 'Fundamentos de álgebra lineal'),
        ('Estadística', 'MAT103', 'Aula 102', 3, 'Estadística descriptiva e inferencial'),
        ('Cálculo Integral', 'MAT104', 'Aula 301', 4, 'Métodos de integración'),
        ('Matemáticas Básicas', 'MAT001', 'Aula 205', 3, 'Fundamentos matemáticos'),
        ('Ecuaciones Diferenciales', 'MAT201', 'Aula 301', 4, 'Ecuaciones diferenciales ordinarias'),
        ('Probabilidad', 'MAT105', 'Aula 301', 3, 'Teoría de probabilidades'),
        ('Probabilidad (Lab)', 'MAT105L', 'Lab 2', 1, 'Laboratorio de probabilidad'),
        ('Estadística (Lab)', 'MAT103L', 'Lab 3', 1, 'Laboratorio de estadística'),
        ('Geometría Analítica', 'MAT106', 'Aula 404', 3, 'Geometría en el plano y espacio'),
        ('Asesorías', 'ASE001', 'Oficina 12', 2, 'Asesorías personalizadas'),
    ]

    for materia in materias:
        cursor.execute("""
            INSERT INTO materias (nombre, codigo, aula, creditos, descripcion)
            VALUES (?, ?, ?, ?, ?)
        """, materia)

    print(f"[OK] {len(materias)} materias insertadas")

    # Asignar algunas materias a docentes (Dr. Carlos Martínez - ID 1)
    asignaciones = [
        (1, 1),  # Cálculo Diferencial -> Dr. Carlos
        (2, 1),  # Álgebra Lineal -> Dr. Carlos
        (3, 1),  # Estadística -> Dr. Carlos
        (4, 1),  # Cálculo Integral -> Dr. Carlos
    ]

    for materia_id, docente_id in asignaciones:
        cursor.execute("UPDATE materias SET docente_id = ? WHERE id = ?", (docente_id, materia_id))

    print(f"[OK] {len(asignaciones)} asignaciones realizadas")

    # Insertar Horarios para las materias asignadas
    horarios = [
        # Cálculo Diferencial (Lunes y Miércoles 08:00-10:00)
        (1, 'Lunes', '08:00', '10:00'),
        (1, 'Miércoles', '08:00', '10:00'),

        # Álgebra Lineal (Lunes y Miércoles 10:00-12:00)
        (2, 'Lunes', '10:00', '12:00'),
        (2, 'Miércoles', '10:00', '12:00'),

        # Estadística (Martes 14:00-16:00)
        (3, 'Martes', '14:00', '16:00'),

        # Cálculo Integral (Miércoles 08:00-10:00)
        (4, 'Miércoles', '08:00', '10:00'),

        # Probabilidad (Viernes 08:00-12:00)
        (7, 'Viernes', '08:00', '12:00'),

        # Probabilidad Lab (Viernes 10:00-12:00)
        (8, 'Viernes', '10:00', '12:00'),

        # Estadística Lab (Martes 14:00-16:00)
        (9, 'Martes', '14:00', '16:00'),

        # Geometría Analítica (Jueves 14:00-18:00)
        (10, 'Jueves', '14:00', '18:00'),

        # Asesorías (Jueves 16:00-18:00)
        (11, 'Jueves', '16:00', '18:00'),
    ]

    for horario in horarios:
        cursor.execute("""
            INSERT INTO horarios (materia_id, dia_semana, hora_inicio, hora_fin)
            VALUES (?, ?, ?, ?)
        """, horario)

    print(f"[OK] {len(horarios)} horarios insertados")

    # Insertar Preferencias para Dr. Carlos
    preferencias = [
        (1, 1, 'Lunes', '08:00 - 12:00', 'Aprobada'),
        (1, 2, 'Lunes', '14:00 - 18:00', 'Aprobada'),
        (1, 3, 'Martes', '08:00 - 12:00', 'Pendiente'),
        (1, 4, 'Miércoles', '08:00 - 12:00', 'Aprobada'),
        (1, 10, 'Jueves', '14:00 - 18:00', 'Pendiente'),
        (1, 7, 'Viernes', '08:00 - 12:00', 'Aprobada'),
    ]

    for pref in preferencias:
        cursor.execute("""
            INSERT INTO preferencias (docente_id, materia_id, dia_semana, horario, estado)
            VALUES (?, ?, ?, ?, ?)
        """, pref)

    print(f"[OK] {len(preferencias)} preferencias insertadas")

    # Insertar algunas notificaciones
    notificaciones = [
        (1, 'Nueva Asignación de Materia', 'Se te ha asignado la materia: Cálculo Diferencial', 'success'),
        (1, 'Preferencia Aprobada', 'Tu preferencia para Álgebra Lineal ha sido aprobada', 'success'),
    ]

    for notif in notificaciones:
        cursor.execute("""
            INSERT INTO notificaciones (usuario_id, titulo, mensaje, tipo)
            VALUES (?, ?, ?, ?)
        """, notif)

    print(f"[OK] {len(notificaciones)} notificaciones insertadas")

    conn.commit()
    conn.close()

    print("\n[OK] Datos de prueba insertados exitosamente")
    print("\nCredenciales de acceso:")
    print("-" * 50)
    print("DOCENTE:")
    print("  Email: docente@demo.com")
    print("  Password: docente123")
    print("\nADMINISTRATIVO:")
    print("  Email: administrativo@demo.com")
    print("  Password: admin123")
    print("-" * 50)


if __name__ == "__main__":
    poblar_datos()
