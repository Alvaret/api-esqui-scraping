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
DEFAULT_STATIONS = ['sierra-nevada', 'baqueira-beret', 'formigal', 'candanchu', 'jaca-astun']


def normalize_metric(value):
    """Normaliza un valor de métrica para devolver un string estable."""
    if value is None:
        return '0'

    cleaned = str(value).strip().replace('\xa0', ' ')
    if cleaned in {'-', '—', '–', ''}:
        return '0'
    return cleaned.replace('/', '').strip()


def parse_metric_block(span, label: str):
    """Extrae un bloque de métricas con el formato esperado por la API."""
    strong = span.select_one('strong.fuentemega, strong.fuentemega.fuenteazul')
    em = span.find('em')

    if label == 'Nieve':
        valor = normalize_metric(strong.get_text(' ', strip=True)) if strong else '0'
        unidad = em.get_text(' ', strip=True) if em else 'cm'
        return {'espesor': valor, 'unidad': unidad}

    abierto = normalize_metric(strong.get_text(' ', strip=True)) if strong else '0'
    total = normalize_metric(em.get_text(' ', strip=True)) if em else '0'
    return {'abiertos': abierto, 'total': total}


def scrape_estacion(slug: str) -> dict:
    """Extrae datos de una estación de esquí."""

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
            'remontes': {'abiertos': '0', 'total': '0'},
            'kilometros': {'abiertos': '0', 'total': '0'},
            'nieve': {'espesor': '0', 'unidad': 'cm'},
            'timestamp': datetime.now().isoformat(),
            'estado': 'success'
        }

        for span in soup.find_all('span'):
            text = span.get_text(' ', strip=True)

            if 'Remontes' in text:
                datos['remontes'] = parse_metric_block(span, 'Remontes')
            elif 'Kilómetros' in text or 'Kilometros' in text:
                datos['kilometros'] = parse_metric_block(span, 'Kilómetros')
            elif 'Nieve' in text:
                datos['nieve'] = parse_metric_block(span, 'Nieve')

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
    """Evento de inicio del servidor."""
    print(f"[{datetime.now()}] Servidor iniciado - scraping se realizará bajo demanda")


# Rutas de la API
@app.get("/")
async def root():
    """Endpoint raíz con información de la API."""
    return {
        "nombre": "Esqui Scraping API",
        "version": "1.0.0",
        "descripcion": "API para obtener información de estaciones de esquí españolas",
        "endpoints": {
            "todas": "/estaciones",
            "por_slug": "/estacion/{slug}",
            "status": "/status",
            "refresh": "/refresh"
        }
    }


@app.get("/estaciones")
async def get_all_estaciones(estaciones: str = None):
    """Obtiene datos de múltiples estaciones (scraping en tiempo real)."""
    global ultima_actualizacion

    if estaciones:
        slugs = [slug.strip() for slug in estaciones.split(',') if slug.strip()]
    else:
        slugs = DEFAULT_STATIONS

    print(f"[{datetime.now()}] Scrapeando estaciones: {', '.join(slugs)}...")

    resultados = [scrape_estacion(slug) for slug in slugs]
    ultima_actualizacion = datetime.now().isoformat()

    return {
        "estaciones": resultados,
        "total": len(resultados),
        "ultima_actualizacion": ultima_actualizacion
    }


@app.post("/refresh")
async def refresh_estaciones():
    """Fuerza la actualización del caché de estaciones."""
    response = await get_all_estaciones()
    return {
        "mensaje": "Caché actualizado",
        "estaciones": response["estaciones"],
        "timestamp": datetime.now().isoformat()
    }


@app.get("/estacion/{slug}")
async def get_estacion(slug: str):
    """Obtiene datos de una estación específica (scraping en tiempo real)."""
    print(f"[{datetime.now()}] Scrapeando {slug}...")
    return scrape_estacion(slug)


@app.get("/status")
async def get_status():
    """Estado de la API."""
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
