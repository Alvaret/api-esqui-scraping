#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend API para web scraping de estaciones de esquí
Desplegado en Railway
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json

# Configuración
app = FastAPI(title="Esqui Scraping API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables globales
ultima_actualizacion = None

# URL base para construir las URLs de las estaciones
BASE_URL = 'https://www.infonieve.es/estacion-esqui/'

def scrape_estacion(slug: str) -> dict:
    """Extrae datos de una estación de esquí"""
    
    # Construir la URL completa
    url = f"{BASE_URL}{slug}/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        datos = {
            'slug': slug,
            'nombre': slug.replace('-', ' ').title(),
            'remontes': None,
            'kilometros': None,
            'nieve': None,
            'timestamp': datetime.now().isoformat(),
            'estado': 'success'
        }
        
        # Extraer datos usando el método que funciona (buscar en todos los spans)
        spans = soup.find_all('span')
        
        for span in spans:
            # Buscar remontes
            if 'Remontes' in span.text:
                strong = span.find('strong', class_='fuentemega')
                em = span.find('em')
                if strong and em:
                    valor = strong.text.strip()
                    max_val = em.text.strip().replace('/', '')
                    datos['remontes'] = f"{valor}/{max_val}"
            
            # Buscar kilómetros
            elif 'Kilómetros' in span.text:
                strong = span.find('strong', class_='fuentemega')
                em = span.find('em')
                if strong and em:
                    valor = strong.text.strip()
                    max_val = em.text.strip().replace('/', '')
                    datos['kilometros'] = f"{valor}/{max_val}"
            
            # Buscar nieve
            elif 'Nieve' in span.text:
                strong = span.find('strong', class_='fuentemega')
                em = span.find('em')
                if strong and em:
                    valor = strong.text.strip()
                    unidad = em.text.strip()
                    datos['nieve'] = f"{valor} {unidad}"
        
        return datos
        
    except requests.exceptions.RequestException as e:
        return {
            'slug': slug,
            'nombre': slug.replace('-', ' ').title(),
            'error': f'Error de conexión: {str(e)}',
            'timestamp': datetime.now().isoformat(),
            'estado': 'error'
        }
    except Exception as e:
        return {
            'slug': slug,
            'nombre': slug.replace('-', ' ').title(),
            'error': f'Error: {str(e)}',
            'timestamp': datetime.now().isoformat(),
            'estado': 'error'
        }

@app.on_event("startup")
async def startup_event():
    """Evento de inicio del servidor"""
    print(f"[{datetime.now()}] Servidor iniciado - scraping se realizará bajo demanda")

# Rutas de la API
@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "nombre": "Esqui Scraping API",
        "version": "1.0.0",
        "descripcion": "API para obtener información de estaciones de esquí españolas",
        "endpoints": {
            "todas": "/estaciones",
            "por_slug": "/estacion/{slug}",
            "status": "/status"
        }
    }

@app.get("/estaciones")
async def get_all_estaciones(estaciones: str = None):
    """Obtiene datos de múltiples estaciones (scraping en tiempo real)
    
    Parámetros:
    - estaciones: Lista de slugs separados por coma (ej: sierra-nevada,candanchu)
    """
    global ultima_actualizacion
    
    if estaciones:
        # Si se proporcionan estaciones específicas
        slugs = [slug.strip() for slug in estaciones.split(',')]
    else:
        # Estaciones por defecto si no se especifica ninguna
        slugs = ['sierra-nevada', 'baqueira-beret', 'formigal', 'candanchu', 'jaca-astun']
    
    print(f"[{datetime.now()}] Scrapeando estaciones: {', '.join(slugs)}...")
    
    resultados = []
    for slug in slugs:
        datos = scrape_estacion(slug)
        resultados.append(datos)
    
    ultima_actualizacion = datetime.now().isoformat()
    
    return {
        "estaciones": resultados,
        "total": len(resultados),
        "ultima_actualizacion": ultima_actualizacion
    }

@app.get("/estacion/{slug}")
async def get_estacion(slug: str):
    """Obtiene datos de una estación específica (scraping en tiempo real)
    
    El slug debe corresponder con el nombre de la URL en infonieve.es
    Ejemplo: sierra-nevada, candanchu, valdelinares, boi-taull, etc.
    """
    
    print(f"[{datetime.now()}] Scrapeando {slug}...")
    return scrape_estacion(slug)

@app.get("/status")
async def get_status():
    """Estado de la API"""
    return {
        "status": "ok",
        "base_url": BASE_URL,
        "descripcion": "Acepta cualquier slug de estación de infonieve.es",
        "ejemplos": ["sierra-nevada", "candanchu", "valdelinares", "boi-taull", "baqueira-beret"],
        "ultima_actualizacion": ultima_actualizacion,
        "timestamp": datetime.now().isoformat()
    }



if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
