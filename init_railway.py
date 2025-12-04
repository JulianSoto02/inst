"""
Inicialización automática de base de datos para Railway
Se ejecuta antes de iniciar gunicorn
"""
import os
import sys

# Verificar si la base de datos existe
db_path = 'database/universidad.db'

if not os.path.exists(db_path):
    print("[Railway] Base de datos no existe. Inicializando...")

    # Crear directorio si no existe
    os.makedirs('database', exist_ok=True)

    # Inicializar base de datos
    print("[Railway] Ejecutando init_db.py...")
    os.system('python database/init_db.py')

    # Poblar con datos demo
    print("[Railway] Ejecutando seed_data.py...")
    os.system('python database/seed_data.py')

    print("[Railway] Base de datos inicializada correctamente")
else:
    print("[Railway] Base de datos ya existe")

print("[Railway] Listo para iniciar gunicorn")
