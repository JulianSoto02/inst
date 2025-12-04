#!/bin/bash

echo "Inicializando base de datos para Railway..."

# Crear directorio de database si no existe
mkdir -p database

# Inicializar la base de datos
python database/init_db.py

# Poblar con datos demo
python database/seed_data.py

echo "Base de datos inicializada correctamente"
