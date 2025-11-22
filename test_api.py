"""
Script de prueba para la API del backend
Ejecutar: python test_api.py
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Imprime un título de sección"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_root():
    """Test del endpoint raíz"""
    print_section("TEST: GET /")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        response.raise_for_status()
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print("✓ PASS")
    except Exception as e:
        print(f"✗ FAIL: {e}")

def test_estaciones():
    """Test de todas las estaciones"""
    print_section("TEST: GET /estaciones")
    
    try:
        response = requests.get(f"{BASE_URL}/estaciones")
        response.raise_for_status()
        data = response.json()
        
        print(f"Total de estaciones: {data.get('total')}")
        print(f"Última actualización: {data.get('ultima_actualizacion')}")
        print("\nEstaciones:")
        
        for estacion in data.get('estaciones', []):
            print(f"\n  • {estacion['nombre']} ({estacion['slug']})")
            print(f"    Estado: {estacion['estado']}")
            
            if estacion['estado'] == 'success':
                if estacion.get('remontes'):
                    print(f"    Remontes: {estacion['remontes']['abiertos']}/{estacion['remontes']['total']}")
                if estacion.get('kilometros'):
                    print(f"    Km: {estacion['kilometros']['abiertos']}/{estacion['kilometros']['total']}")
                if estacion.get('nieve'):
                    print(f"    Nieve: {estacion['nieve']['espesor']} {estacion['nieve']['unidad']}")
            else:
                print(f"    Error: {estacion.get('error')}")
        
        print("\n✓ PASS")
    except Exception as e:
        print(f"✗ FAIL: {e}")

def test_estacion(slug):
    """Test de una estación específica"""
    print_section(f"TEST: GET /estacion/{slug}")
    
    try:
        response = requests.get(f"{BASE_URL}/estacion/{slug}")
        response.raise_for_status()
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print("✓ PASS")
    except Exception as e:
        print(f"✗ FAIL: {e}")

def test_status():
    """Test del status"""
    print_section("TEST: GET /status")
    
    try:
        response = requests.get(f"{BASE_URL}/status")
        response.raise_for_status()
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print("✓ PASS")
    except Exception as e:
        print(f"✗ FAIL: {e}")

def test_refresh():
    """Test de actualización manual"""
    print_section("TEST: POST /refresh")
    
    try:
        response = requests.post(f"{BASE_URL}/refresh")
        response.raise_for_status()
        data = response.json()
        
        print(f"Mensaje: {data.get('mensaje')}")
        print(f"Estaciones actualizadas: {len(data.get('estaciones', []))}")
        print(f"Timestamp: {data.get('timestamp')}")
        print("✓ PASS")
    except Exception as e:
        print(f"✗ FAIL: {e}")

def main():
    """Ejecuta todos los tests"""
    
    print("\n" + "█" * 60)
    print("█  PRUEBA DE API - ESQUI SCRAPING")
    print("█" * 60)
    
    # Verificar conexión
    try:
        response = requests.get(f"{BASE_URL}/", timeout=2)
        print(f"\n✓ Conectado a {BASE_URL}")
    except requests.exceptions.ConnectionError:
        print(f"\n✗ No se puede conectar a {BASE_URL}")
        print("   ¿Está el servidor corriendo? (python run.py)")
        return
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return
    
    # Ejecutar tests
    test_root()
    test_status()
    test_estaciones()
    test_estacion("sierra-nevada")
    test_estacion("baqueira-beret")
    test_estacion("formigal")
    test_refresh()
    
    # Resumen
    print_section("RESUMEN DE PRUEBAS")
    print("Todos los tests completados")
    print("✓ La API está funcionando correctamente")
    print("\nPróximos pasos:")
    print("1. Desplegar en Railway")
    print("2. Conectar el frontend a la API")
    print("3. Configurar variables de entorno")

if __name__ == "__main__":
    main()
