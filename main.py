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

# Estaciones disponibles
ESTACIONES = {
    'sierra-nevada': 'https://www.infonieve.es/estacion-esqui/sierra-nevada/',
    'baqueira-beret': 'https://www.infonieve.es/estacion-esqui/baqueira-beret/',
    'formigal': 'https://www.infonieve.es/estacion-esqui/formigal/',
    'candanchu': 'https://www.infonieve.es/estacion-esqui/candanchu/',
    'jaca-astun': 'https://www.infonieve.es/estacion-esqui/jaca-astun/',
}

def scrape_estacion(slug: str, url: str) -> dict:
    """Extrae datos de una estación de esquí"""
    
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
async def get_all_estaciones():
    """Obtiene datos de todas las estaciones (scraping en tiempo real)"""
    global ultima_actualizacion
    
    print(f"[{datetime.now()}] Scrapeando todas las estaciones...")
    
    estaciones = []
    for slug, url in ESTACIONES.items():
        datos = scrape_estacion(slug, url)
        estaciones.append(datos)
    
    ultima_actualizacion = datetime.now().isoformat()
    
    return {
        "estaciones": estaciones,
        "total": len(estaciones),
        "ultima_actualizacion": ultima_actualizacion
    }

@app.get("/estacion/{slug}")
async def get_estacion(slug: str):
    """Obtiene datos de una estación específica (scraping en tiempo real)"""
    
    if slug not in ESTACIONES:
        return {
            "error": f"Estación '{slug}' no encontrada",
            "estaciones_disponibles": list(ESTACIONES.keys())
        }
    
    print(f"[{datetime.now()}] Scrapeando {slug}...")
    url = ESTACIONES[slug]
    return scrape_estacion(slug, url)

@app.get("/status")
async def get_status():
    """Estado de la API"""
    return {
        "status": "ok",
        "estaciones_disponibles": len(ESTACIONES),
        "ultima_actualizacion": ultima_actualizacion,
        "timestamp": datetime.now().isoformat()
    }



if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
