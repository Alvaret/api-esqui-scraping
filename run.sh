#!/bin/bash
# Script para iniciar el backend en macOS/Linux

cd "$(dirname "$0")"

echo ""
echo "============================================================"
echo "              INICIANDO BACKEND ESQUI SCRAPING"
echo "============================================================"
echo ""

# Verificar que estamos en la carpeta correcta
if [ ! -f requirements.txt ]; then
    echo "❌ Error: requirements.txt no encontrado"
    echo "   Asegúrate de ejecutar esto desde la carpeta 'backend'"
    exit 1
fi

# Crear venv si no existe
if [ ! -d venv ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar venv
source venv/bin/activate

# Instalar dependencias
echo "Verificando dependencias..."
pip install -q -r requirements.txt

echo ""
echo "[✓] Servidor disponible en: http://localhost:8000"
echo "[✓] Documentación: http://localhost:8000/docs"
echo "[✓] Presiona Ctrl+C para detener"
echo ""

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
