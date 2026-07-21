"""Analysefunktionen für Dashboard, Streaming-Ansicht und Evaluation.

Enthält deskriptive Kennzahlen je Stadt, die Korrelationsmatrix,
Tagesprofile sowie ergänzende analytische Hilfen (gleitender Mittelwert
und einfache Ausreißererkennung), die im Dashboard genutzt werden können.
"""
from __future__ import annotations

import pandas as pd

from config import NUMERIC_COLUMNS


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Berechnet die Pearson-Korrelationsmatrix der verfügbaren Messgrößen."""
    available = [col for col in NUMERIC_COLUMNS if col in df.columns]
    if len(available) < 2:
        return pd.DataFrame()
    numeric = df[available]
    # Spalten ohne Varianz entfernen (z. B. außerhalb der Saison konstant 0
    # gemeldete Pollenarten); ihre Korrelation wäre sonst undefiniert (NaN).
    keep = numeric.std(numeric_only=True) > 0
    numeric = numeric.loc[:, keep[keep].index]
    if numeric.shape[1] < 2:
        return pd.DataFrame()
    return numeric.corr(numeric_only=True).round(3)


def city_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregiert zentrale Kennzahlen je Stadt."""
    if df.empty:
        return pd.DataFrame()
    return (
        df.groupby("city", as_index=False)
        .agg(
            records=("timestamp", "count"),
            avg_temperature=("temperature_2m", "mean"),
            total_precipitation=("precipitation", "sum"),
            avg_pm2_5=("pm2_5", "mean"),
            avg_pm10=("pm10", "mean"),
            avg_european_aqi=("european_aqi", "mean"),
            max_european_aqi=("european_aqi", "max"),
        )
        .round(2)
    )


def hourly_profile(df: pd.DataFrame, value: str = "pm2_5") -> pd.DataFrame:
    """Bildet den Tagesgang (Mittelwert je Stunde) einer Messgröße je Stadt."""
    if df.empty or value not in df.columns or "hour" not in df.columns:
        return pd.DataFrame()
    return (
        df.groupby(["city", "hour"], as_index=False)[value]
        .mean()
        .rename(columns={value: f"avg_{value}"})
        .round(2)
    )


def rolling_average(df: pd.DataFrame, value: str = "pm2_5", window: int = 6) -> pd.DataFrame:
    """Berechnet je Stadt einen gleitenden Mittelwert zur Glättung von Zeitreihen."""
    if df.empty or value not in df.columns:
        return pd.DataFrame()
    out = df.sort_values(["city", "timestamp"]).copy()
    out[f"{value}_rolling"] = (
        out.groupby("city")[value].transform(lambda s: s.rolling(window, min_periods=1).mean())
    )
    return out[["timestamp", "city", value, f"{value}_rolling"]]


def flag_outliers(df: pd.DataFrame, value: str = "european_aqi", z: float = 3.0) -> pd.DataFrame:
    """Markiert Werte, die je Stadt mehr als z Standardabweichungen abweichen."""
    if df.empty or value not in df.columns:
        return pd.DataFrame()
    out = df.copy()
    grp = out.groupby("city")[value]
    zscore = (out[value] - grp.transform("mean")) / grp.transform("std").replace(0, pd.NA)
    out["is_outlier"] = zscore.abs() > z
    return out[out["is_outlier"]][["timestamp", "city", value]]
