@echo off
REM Script para iniciar el backend en Windows

title Esqui Scraping API

echo.
echo ============================================================
echo              INICIANDO BACKEND ESQUI SCRAPING
echo ============================================================
echo.

REM Verificar que estamos en la carpeta correcta
if not exist requirements.txt (
    echo ERROR: requirements.txt no encontrado
    echo Asegurate de ejecutar esto desde la carpeta 'backend'
    pause
    exit /b 1
)

REM Verificar si el venv existe
if not exist venv (
    echo Creando entorno virtual...
    python -m venv venv
)

REM Activar venv
call venv\Scripts\activate.bat

REM Instalar dependencias si es necesario
echo Verificando dependencias...
pip install -q -r requirements.txt

REM Iniciar servidor
echo.
echo [*] Servidor disponible en: http://localhost:8000
echo [*] Documentacion: http://localhost:8000/docs
echo [*] Presiona Ctrl+C para detener
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
