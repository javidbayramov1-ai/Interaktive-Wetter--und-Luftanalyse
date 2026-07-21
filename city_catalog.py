"""Persistenzschicht (SQLite).

Gegenüber dem ersten Prototyp wurde die Speicherung von "Tabelle bei
jedem Lauf ersetzen" auf ein echtes Upsert umgestellt. Die Tabelle
``measurements`` besitzt einen Primärschlüssel aus (city, timestamp);
neue Abrufe ergänzen den Bestand, statt ihn zu überschreiben, und
doppelte Zeitstempel werden automatisch aktualisiert. Erst dadurch lässt
sich eine über die Zeit wachsende Zeitreihe aufbauen – die Grundlage für
den Streaming-Betrieb und für einen täglichen Batch-Job.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from config import CANONICAL_COLUMNS, DEFAULT_DB_PATH, MEASUREMENTS_TABLE


def ensure_parent(path: Path) -> None:
    """Legt den übergeordneten Ordner der Datenbankdatei an, falls nötig."""
    path.parent.mkdir(parents=True, exist_ok=True)


def _column_definitions() -> str:
    """Erzeugt die Spaltendefinition für das CREATE-TABLE-Statement."""
    defs = []
    for col in CANONICAL_COLUMNS:
        if col in ("timestamp", "city", "mode", "ingested_at"):
            defs.append(f'"{col}" TEXT')
        else:
            defs.append(f'"{col}" REAL')
    return ", ".join(defs)


def ensure_table(con: sqlite3.Connection) -> None:
    """Stellt sicher, dass die Tabelle mit Primärschlüssel existiert."""
    con.execute(
        f'CREATE TABLE IF NOT EXISTS "{MEASUREMENTS_TABLE}" '
        f"({_column_definitions()}, PRIMARY KEY (city, timestamp))"
    )


def _table_exists(con: sqlite3.Connection, name: str) -> bool:
    row = con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone()
    return row is not None


def _prepare_frame(df: pd.DataFrame, mode: str) -> pd.DataFrame:
    """Bringt einen DataFrame auf das kanonische Speicherformat."""
    out = df.copy()
    out["timestamp"] = pd.to_datetime(out["timestamp"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    out["mode"] = mode
    out["ingested_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    # Fehlende kanonische Spalten ergänzen, überzählige verwerfen, Reihenfolge fixieren.
    return out.reindex(columns=CANONICAL_COLUMNS)


def save_measurements(df: pd.DataFrame, db_path: Path = DEFAULT_DB_PATH, mode: str = "batch") -> int:
    """Schreibt Messwerte per Upsert in die Datenbank und gibt deren Anzahl zurück.

    Vorhandene Zeilen mit gleichem (city, timestamp) werden ersetzt
    (INSERT OR REPLACE), alle anderen ergänzt. So bleibt der Bestand über
    mehrere Abrufe hinweg erhalten.
    """
    if df is None or df.empty:
        return 0
    ensure_parent(db_path)
    prepared = _prepare_frame(df, mode)
    placeholders = ", ".join("?" for _ in CANONICAL_COLUMNS)
    columns = ", ".join(f'"{c}"' for c in CANONICAL_COLUMNS)
    rows = list(prepared.itertuples(index=False, name=None))
    with sqlite3.connect(db_path) as con:
        ensure_table(con)
        con.executemany(
            f'INSERT OR REPLACE INTO "{MEASUREMENTS_TABLE}" ({columns}) VALUES ({placeholders})',
            rows,
        )
    return len(rows)


def load_measurements(db_path: Path = DEFAULT_DB_PATH) -> pd.DataFrame:
    """Lädt alle gespeicherten Messwerte als DataFrame (Zeitstempel geparst)."""
    if not db_path.exists():
        return pd.DataFrame()
    with sqlite3.connect(db_path) as con:
        if not _table_exists(con, MEASUREMENTS_TABLE):
            return pd.DataFrame()
        df = pd.read_sql_query(f'SELECT * FROM "{MEASUREMENTS_TABLE}"', con)
    if not df.empty and "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def count_measurements(db_path: Path = DEFAULT_DB_PATH) -> int:
    """Zählt die gespeicherten Datensätze (0, falls noch keine Tabelle existiert)."""
    if not db_path.exists():
        return 0
    with sqlite3.connect(db_path) as con:
        if not _table_exists(con, MEASUREMENTS_TABLE):
            return 0
        return int(con.execute(f'SELECT COUNT(*) FROM "{MEASUREMENTS_TABLE}"').fetchone()[0])


def list_tables(db_path: Path = DEFAULT_DB_PATH) -> list[str]:
    """Listet alle Tabellennamen der Datenbank auf."""
    if not db_path.exists():
        return []
    with sqlite3.connect(db_path) as con:
        rows = con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
    return [row[0] for row in rows]
