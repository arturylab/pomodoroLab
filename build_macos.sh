#!/bin/bash
# build_macos.sh

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements-macos.txt

# Limpiar builds anteriores
rm -rf build dist

# Construir la aplicación
python3 setup.py py2app
