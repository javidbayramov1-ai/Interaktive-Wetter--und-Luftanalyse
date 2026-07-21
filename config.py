"""Datenaufbereitung (Feature Engineering) und Datenqualität.

Aus den rohen Messwerten werden Zusatzmerkmale abgeleitet, die Analyse
und Visualisierung erleichtern (z. B. Stunde, Wochentag, Stoßzeit,
AQI-Kategorie). Alle Ableitungen sind gegen fehlende Quellspalten
abgesichert, damit auch unvollständige Live-Events verarbeitet werden
können.
"""
from __future__ import annotations

import pandas as pd

from config import AQI_BINS, AQI_LABELS, NUMERIC_COLUMNS, RUSH_HOURS

# Re-Export für Module, die NUMERIC_COLUMNS bisher aus features importieren.
__all__ = ["NUMERIC_COLUMNS", "enrich", "data_quality_report"]


def enrich(df: pd.DataFrame) -> pd.DataFrame:
    """Ergänzt einen Messwert-DataFrame um abgeleitete Merkmale."""
    if df.empty:
        return df
    result = df.copy()
    result["timestamp"] = pd.to_datetime(result["timestamp"])
    result["date"] = result["timestamp"].dt.date
    result["hour"] = result["timestamp"].dt.hour
    _de_days = {
        "Monday": "Montag", "Tuesday": "Dienstag", "Wednesday": "Mittwoch",
        "Thursday": "Donnerstag", "Friday": "Freitag", "Saturday": "Samstag",
        "Sunday": "Sonntag",
    }
    result["weekday"] = result["timestamp"].dt.day_name().map(_de_days)
    result["is_rush_hour"] = result["hour"].isin(RUSH_HOURS)

    # Niederschlagsflag nur, wenn die Spalte vorhanden ist.
    if "precipitation" in result.columns:
        result["has_precipitation"] = result["precipitation"].fillna(0) > 0

    # AQI-Kategorie nur, wenn der EU-AQI vorhanden ist.
    if "european_aqi" in result.columns:
        result["aqi_category"] = pd.cut(
            result["european_aqi"], bins=AQI_BINS, labels=AQI_LABELS
        )
    return result


def data_quality_report(df: pd.DataFrame) -> pd.DataFrame:
    """Erstellt eine Übersicht fehlender Werte je Spalte (Anzahl und Prozent)."""
    if df.empty:
        return pd.DataFrame(columns=["column", "missing_values", "missing_percent"])
    return pd.DataFrame({
        "column": df.columns,
        "missing_values": [int(df[col].isna().sum()) for col in df.columns],
        "missing_percent": [round(float(df[col].isna().mean() * 100), 2) for col in df.columns],
    })
