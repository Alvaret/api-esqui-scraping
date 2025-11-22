#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar el backend localmente
"""

import subprocess
import sys
import os

def main():
    """Inicia el servidor de desarrollo"""
    
    print("=" * 60)
    print("INICIANDO BACKEND ESQUI SCRAPING API")
    print("=" * 60)
    print()
    
    # Verificar que estamos en la carpeta correcta
    if not os.path.exists("requirements.txt"):
        print("❌ Error: requirements.txt no encontrado")
        print("   Asegúrate de ejecutar esto desde la carpeta 'backend'")
        sys.exit(1)
    
    # Verificar si Python está disponible
    try:
        import fastapi
        print("✓ FastAPI instalado")
    except ImportError:
        print("⚠️  FastAPI no instalado")
        print("   Ejecuta: pip install -r requirements.txt")
        sys.exit(1)
    
    print()
    print("🚀 Iniciando servidor...")
    print()
    print("📍 API disponible en: http://localhost:8000")
    print("📚 Documentación: http://localhost:8000/docs")
    print("📊 Alternativa: http://localhost:8000/redoc")
    print()
    print("Endpoints:")
    print("  GET  http://localhost:8000/estaciones")
    print("  GET  http://localhost:8000/estacion/sierra-nevada")
    print("  GET  http://localhost:8000/status")
    print("  POST http://localhost:8000/refresh")
    print()
    print("Presiona Ctrl+C para detener")
    print()
    
    # Iniciar servidor
    os.system("python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    main()
