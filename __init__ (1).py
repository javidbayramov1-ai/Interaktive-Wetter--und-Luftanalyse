"""Zentrale Konfiguration des Projekts.

Alle an einer Stelle bündelbaren Einstellungen (Variablen, Pfade,
Streaming-Intervall, Schwellenwerte) liegen hier, damit sie nur an einem
Ort geändert werden müssen und nicht über mehrere Module verstreut sind.
"""
from __future__ import annotations

from pathlib import Path

# --- Datenbank ---------------------------------------------------------
# Produktive Datenbank, in der Batch- und Streaming-Daten gemeinsam landen.
DEFAULT_DB_PATH = Path("data/weather_air_quality.sqlite")
MEASUREMENTS_TABLE = "measurements"

# --- Messgrößen --------------------------------------------------------
# Wettervariablen der Open-Meteo-Wetter-API (stündlich bzw. aktuell).
WEATHER_VARIABLES = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m",
]

# Luftqualitätsvariablen der Open-Meteo-Luftqualitäts-API.
AIR_QUALITY_VARIABLES = [
    "pm10",
    "pm2_5",
    "nitrogen_dioxide",
    "ozone",
    "european_aqi",
]

# Zweite Datenquelle: Pollendaten der Open-Meteo-Luftqualitäts-API (CAMS,
# nur Europa, Einheit Pollen/m³). Sie bilden einen biologischen Datensatz,
# der mit Wetter und Luftqualität korreliert werden kann.
POLLEN_VARIABLES = [
    "alder_pollen",
    "birch_pollen",
    "grass_pollen",
    "ragweed_pollen",
]

# Alle numerischen Messgrößen, die analysiert und korreliert werden.
NUMERIC_COLUMNS = WEATHER_VARIABLES + AIR_QUALITY_VARIABLES + POLLEN_VARIABLES

# Kanonische Spaltenreihenfolge eines Messwert-Datensatzes (eine Zeile je
# Stadt und Zeitstempel). 'mode' unterscheidet Batch- von Live-Daten.
CANONICAL_COLUMNS = ["timestamp", "city"] + NUMERIC_COLUMNS + ["mode", "ingested_at"]

# --- Streaming ---------------------------------------------------------
# Standard-Abfrageintervall des Live-Producers in Sekunden.
STREAM_INTERVAL_SECONDS = 300

# --- Fachliche Schwellenwerte -----------------------------------------
# Stunden, die als Stoßzeit (Rush Hour) gewertet werden.
RUSH_HOURS = [7, 8, 16, 17, 18]

# Grenzen und Bezeichner der EU-AQI-Kategorien (untere Grenze exklusiv).
AQI_BINS = [-1, 20, 40, 60, 80, 100, float("inf")]
AQI_LABELS = ["gut", "befriedigend", "mäßig", "schlecht", "sehr schlecht", "extrem schlecht"]


# --------------------------------------------------------------------------
# Deutsche Anzeigenamen (Aliasse) für eine durchgängig deutsche Oberfläche.
# Interne Spaltennamen bleiben unverändert; angezeigt werden diese Klartexte.
# --------------------------------------------------------------------------
DISPLAY_NAMES = {
    # Schlüssel-/Metaspalten
    "timestamp": "Zeitpunkt",
    "city": "Stadt",
    "mode": "Modus",
    "ingested_at": "Gespeichert am",
    # Wetter
    "temperature_2m": "Temperatur (°C)",
    "relative_humidity_2m": "Luftfeuchtigkeit (%)",
    "precipitation": "Niederschlag (mm)",
    "wind_speed_10m": "Windgeschwindigkeit (km/h)",
    # Luftqualität
    "pm10": "Feinstaub PM10 (µg/m³)",
    "pm2_5": "Feinstaub PM2.5 (µg/m³)",
    "nitrogen_dioxide": "Stickstoffdioxid NO₂ (µg/m³)",
    "ozone": "Ozon O₃ (µg/m³)",
    "european_aqi": "EU-Luftqualitätsindex",
    # Pollen (zweite Datenquelle)
    "alder_pollen": "Erlenpollen (Pollen/m³)",
    "birch_pollen": "Birkenpollen (Pollen/m³)",
    "grass_pollen": "Gräserpollen (Pollen/m³)",
    "ragweed_pollen": "Ambrosiapollen (Pollen/m³)",
    # Abgeleitete Merkmale
    "date": "Datum",
    "hour": "Stunde",
    "weekday": "Wochentag",
    "is_rush_hour": "Stoßzeit",
    "has_precipitation": "Niederschlag vorhanden",
    "aqi_category": "AQI-Kategorie",
    # Kennzahlen je Stadt (city_summary)
    "records": "Datensätze",
    "avg_temperature": "Ø Temperatur (°C)",
    "total_precipitation": "Niederschlag gesamt (mm)",
    "avg_pm2_5": "Ø Feinstaub PM2.5 (µg/m³)",
    "avg_pm10": "Ø Feinstaub PM10 (µg/m³)",
    "avg_european_aqi": "Ø EU-Luftqualitätsindex",
    "max_european_aqi": "Max EU-Luftqualitätsindex",
    # Datenqualitätsbericht
    "column": "Spalte",
    "missing_values": "Fehlende Werte",
    "missing_percent": "Fehlend (%)",
}

# Kurzbeschriftungen für die Heatmap (Achsen sonst zu eng).
SHORT_LABELS = {
    "temperature_2m": "Temp.",
    "relative_humidity_2m": "Luftf.",
    "precipitation": "Niedersch.",
    "wind_speed_10m": "Wind",
    "pm10": "PM10",
    "pm2_5": "PM2.5",
    "nitrogen_dioxide": "NO₂",
    "ozone": "Ozon",
    "european_aqi": "EU-AQI",
    "alder_pollen": "Erle",
    "birch_pollen": "Birke",
    "grass_pollen": "Gräser",
    "ragweed_pollen": "Ambrosia",
}
