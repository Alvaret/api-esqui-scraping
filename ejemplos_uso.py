"""
Ejemplos de uso de la API
Guía para desarrolladores
"""

import requests
import json
from datetime import datetime

# URLs
LOCAL_API = "http://localhost:8000"
RAILWAY_API = "https://tu-proyecto.up.railway.app"  # Reemplazar con tu URL

# Usar según ambiente
API_URL = LOCAL_API  # Cambiar a RAILWAY_API para producción

# ============================================================
# EJEMPLO 1: Obtener todas las estaciones
# ============================================================

def get_all_stations():
    """Obtiene datos de todas las estaciones"""
    
    response = requests.get(f"{API_URL}/estaciones")
    data = response.json()
    
    print("TODAS LAS ESTACIONES")
    print("-" * 50)
    
    for estacion in data['estaciones']:
        print(f"\n{estacion['nombre']}")
        print(f"  Remontes: {estacion['remontes']['abiertos']}/{estacion['remontes']['total']}")
        print(f"  Km: {estacion['kilometros']['abiertos']}/{estacion['kilometros']['total']}")
        print(f"  Nieve: {estacion['nieve']['espesor']} {estacion['nieve']['unidad']}")

# ============================================================
# EJEMPLO 2: Obtener una estación específica
# ============================================================

def get_single_station(slug):
    """Obtiene datos de una estación"""
    
    response = requests.get(f"{API_URL}/estacion/{slug}")
    data = response.json()
    
    print(f"\n{data['nombre']}")
    print("=" * 50)
    
    if data['estado'] == 'success':
        print(f"Remontes: {data['remontes']['abiertos']}/{data['remontes']['total']} abiertos")
        print(f"Kilómetros: {data['kilometros']['abiertos']}/{data['kilometros']['total']} km")
        print(f"Nieve: {data['nieve']['espesor']} {data['nieve']['unidad']}")
        print(f"Actualizado: {data['timestamp']}")
    else:
        print(f"Error: {data['error']}")

# ============================================================
# EJEMPLO 3: Monitorear cambios
# ============================================================

def monitor_station(slug, interval_seconds=60):
    """Monitorea una estación y notifica cambios"""
    
    import time
    
    previous_data = None
    
    while True:
        response = requests.get(f"{API_URL}/estacion/{slug}")
        data = response.json()
        
        if data['estado'] == 'success':
            current_remontes = int(data['remontes']['abiertos'])
            
            if previous_data:
                previous_remontes = int(previous_data['remontes']['abiertos'])
                
                if current_remontes != previous_remontes:
                    change = "⬆️" if current_remontes > previous_remontes else "⬇️"
                    print(f"{datetime.now()} | {change} Remontes: {previous_remontes} → {current_remontes}")
            else:
                print(f"{datetime.now()} | Remontes: {current_remontes}")
            
            previous_data = data
        
        time.sleep(interval_seconds)

# ============================================================
# EJEMPLO 4: Comparar estaciones
# ============================================================

def compare_stations(slugs):
    """Compara múltiples estaciones"""
    
    estaciones = []
    
    for slug in slugs:
        response = requests.get(f"{API_URL}/estacion/{slug}")
        estaciones.append(response.json())
    
    # Encabezados
    print("\nCOMPARACIÓN DE ESTACIONES")
    print("=" * 80)
    print(f"{'Estación':<20} {'Remontes':<15} {'Km':<15} {'Nieve':<15}")
    print("-" * 80)
    
    # Datos
    for est in estaciones:
        if est['estado'] == 'success':
            nom = est['nombre'][:19]
            rem = f"{est['remontes']['abiertos']}/{est['remontes']['total']}"
            km = f"{est['kilometros']['abiertos']}/{est['kilometros']['total']}"
            nieve = f"{est['nieve']['espesor']} {est['nieve']['unidad'][:2]}"
            
            print(f"{nom:<20} {rem:<15} {km:<15} {nieve:<15}")

# ============================================================
# EJEMPLO 5: Obtener estación con mejor nieve
# ============================================================

def find_best_snow():
    """Encuentra la estación con más nieve"""
    
    response = requests.get(f"{API_URL}/estaciones")
    data = response.json()
    
    best = None
    max_nieve = 0
    
    for estacion in data['estaciones']:
        if estacion['estado'] == 'success':
            nieve = int(estacion['nieve']['espesor'])
            if nieve > max_nieve:
                max_nieve = nieve
                best = estacion
    
    if best:
        print(f"\n🏔️  MEJOR NIEVE: {best['nombre']}")
        print(f"   Nieve: {best['nieve']['espesor']} {best['nieve']['unidad']}")
        print(f"   Remontes: {best['remontes']['abiertos']}/{best['remontes']['total']}")

# ============================================================
# EJEMPLO 6: Exportar datos a JSON
# ============================================================

def export_to_json(filename="estaciones.json"):
    """Exporta datos a archivo JSON"""
    
    response = requests.get(f"{API_URL}/estaciones")
    data = response.json()
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Datos exportados a {filename}")

# ============================================================
# EJEMPLO 7: Integración con bot de Discord
# ============================================================

def get_discord_embed():
    """Obtiene datos formateados para Discord"""
    
    response = requests.get(f"{API_URL}/estaciones")
    data = response.json()
    
    embeds = []
    
    for estacion in data['estaciones']:
        if estacion['estado'] == 'success':
            embed = {
                "title": estacion['nombre'],
                "fields": [
                    {
                        "name": "Remontes",
                        "value": f"{estacion['remontes']['abiertos']}/{estacion['remontes']['total']}",
                        "inline": True
                    },
                    {
                        "name": "Km",
                        "value": f"{estacion['kilometros']['abiertos']}/{estacion['kilometros']['total']}",
                        "inline": True
                    },
                    {
                        "name": "Nieve",
                        "value": f"{estacion['nieve']['espesor']} {estacion['nieve']['unidad']}",
                        "inline": False
                    }
                ],
                "timestamp": estacion['timestamp']
            }
            embeds.append(embed)
    
    return embeds

# ============================================================
# EJEMPLO 8: Crear tabla para web
# ============================================================

def generate_html_table():
    """Genera tabla HTML con los datos"""
    
    response = requests.get(f"{API_URL}/estaciones")
    data = response.json()
    
    html = """
    <table>
        <thead>
            <tr>
                <th>Estación</th>
                <th>Remontes</th>
                <th>Km</th>
                <th>Nieve</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for estacion in data['estaciones']:
        if estacion['estado'] == 'success':
            html += f"""
            <tr>
                <td>{estacion['nombre']}</td>
                <td>{estacion['remontes']['abiertos']}/{estacion['remontes']['total']}</td>
                <td>{estacion['kilometros']['abiertos']}/{estacion['kilometros']['total']}</td>
                <td>{estacion['nieve']['espesor']} {estacion['nieve']['unidad']}</td>
            </tr>
            """
    
    html += """
        </tbody>
    </table>
    """
    
    return html

# ============================================================
# MAIN - Ejecutar ejemplos
# ============================================================

if __name__ == "__main__":
    
    print("EJEMPLOS DE USO - API ESQUI SCRAPING")
    print("=" * 60)
    print()
    
    # Verificar conexión
    try:
        requests.get(f"{API_URL}/", timeout=2)
    except:
        print(f"ERROR: No se puede conectar a {API_URL}")
        print("Asegúrate de que el servidor esté corriendo")
        exit(1)
    
    # Ejecutar ejemplos
    print("\n1. Obtener todas las estaciones:")
    get_all_stations()
    
    print("\n\n2. Obtener una estación específica:")
    get_single_station("sierra-nevada")
    
    print("\n\n3. Comparar estaciones:")
    compare_stations(["sierra-nevada", "baqueira-beret", "formigal"])
    
    print("\n\n4. Encontrar mejor nieve:")
    find_best_snow()
    
    print("\n\n5. Exportar a JSON:")
    export_to_json()
    
    print("\n\n6. Generar tabla HTML:")
    html = generate_html_table()
    print("HTML generado (primeras 200 caracteres):")
    print(html[:200] + "...")
    
    print("\n\n" + "=" * 60)
    print("✓ Ejemplos completados")
    print("\nOtros ejemplos disponibles:")
    print("  - monitor_station(): Monitorear cambios en tiempo real")
    print("  - get_discord_embed(): Formatear para Discord")
