"""Städtekatalog mit geographischen Koordinaten.

Die Koordinaten werden für die Abfrage der Open-Meteo-APIs benötigt, die
Daten anhand von Breiten- und Längengrad liefern. Weitere Städte lassen
sich einfach durch Ergänzen eines Eintrags hinzufügen.
"""
from __future__ import annotations

CITY_COORDS: dict[str, dict[str, float]] = {
    "Aalen": {"latitude": 48.8378, "longitude": 10.0933},
    "Stuttgart": {"latitude": 48.7758, "longitude": 9.1829},
    "Berlin": {"latitude": 52.5200, "longitude": 13.4050},
    "Hamburg": {"latitude": 53.5511, "longitude": 9.9937},
    "Munich": {"latitude": 48.1351, "longitude": 11.5820},
    "Frankfurt am Main": {"latitude": 50.1109, "longitude": 8.6821},
    "Cologne": {"latitude": 50.9375, "longitude": 6.9603},
    "Leipzig": {"latitude": 51.3397, "longitude": 12.3731},
}
