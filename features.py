"""Zweite Datenquelle: Pollendaten (Open-Meteo Luftqualitäts-/CAMS-API).

Als zweiter, fachlich eigenständiger Datensatz werden Pollenkonzentrationen
abgerufen. Pollen sind ein biologischer Datensatz (Allergenbelastung) und
eignen sich gut zur Korrelation mit Wetter- und Luftqualitätsvariablen:
Pollen steigen typischerweise mit Wärme und Wind und werden durch Regen aus
der Luft gewaschen.

Hinweise:
* Pollen liefert Open-Meteo nur für Europa (CAMS-Modell), Einheit Pollen/m³.
* Pollen sind saisonal: Im Sommer dominiert Gräserpollen, Birke/Erle sind
  dann nahezu null. Für aussagekräftige Korrelationen einen Zeitraum mit
  aktiver Pollenart wählen.
* Die historische Tiefe ist geringer als bei den ERA5-Wetterdaten.
"""
from __future__ import annotations

import pandas as pd

from config import POLLEN_VARIABLES
from src.open_meteo import (
    AIR_QUALITY_ENDPOINT,
    Location,
    _get_json,
    _hourly_payload_to_frame,
)


def fetch_pollen(location: Location, start_date: str, end_date: str) -> pd.DataFrame:
    """Lädt Pollendaten einer Stadt für den Zeitraum (Batch)."""
    params = {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ",".join(POLLEN_VARIABLES),
        "timezone": "Europe/Berlin",
        "domains": "auto",
    }
    payload = _get_json(AIR_QUALITY_ENDPOINT, params)
    return _hourly_payload_to_frame(payload, location.city, "pollen")


def fetch_pollen_current(location: Location) -> dict:
    """Ruft die aktuellen Pollenwerte einer Stadt ab (für das Streaming)."""
    payload = _get_json(AIR_QUALITY_ENDPOINT, {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "current": ",".join(POLLEN_VARIABLES),
        "timezone": "Europe/Berlin",
        "domains": "auto",
    })
    return payload.get("current", {})


def pollen_preview_url(location: Location, start_date: str, end_date: str) -> str:
    """Erzeugt die vollständige Abruf-URL für die Pollendaten (Doku)."""
    from urllib.parse import urlencode
    params = {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ",".join(POLLEN_VARIABLES),
        "timezone": "Europe/Berlin",
        "domains": "auto",
    }
    return f"{AIR_QUALITY_ENDPOINT}?{urlencode(params)}"
