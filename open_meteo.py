"""Streaming-Schicht: kontinuierliche Aufnahme aktueller Messwerte.

Diese leichtgewichtige Streaming-Pipeline kommt ohne zusätzliche
Infrastruktur (Kafka, Spark) aus und ist mit reinem Python lauffähig:

    Producer  ->  Event(s)  ->  Consumer  ->  SQLite (mode='live')

* Der **Producer** (``poll_once``) fragt in festen Intervallen den
  aktuellen Zustand aller Städte über Open-Meteo ab und erzeugt je Stadt
  ein Event.
* Der **Consumer** (``ingest``) schreibt die Events per Upsert in die
  Datenbank; das Dashboard liest denselben Bestand nahezu live.

Es werden ausschließlich echte Daten verwendet, eine Internetverbindung
ist daher erforderlich.

Start:
    python -m src.streaming --cities Aalen Berlin --interval 300
    python -m src.streaming --interval 600 --iterations 24
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

from config import DEFAULT_DB_PATH, STREAM_INTERVAL_SECONDS
from src.city_catalog import CITY_COORDS
from src.live_client import Event, events_to_frame, fetch_current
from src.open_meteo import Location
from src.storage import count_measurements, save_measurements


def _locations(cities: list[str]) -> list[Location]:
    """Erzeugt Location-Objekte für die gewünschten Städte."""
    return [
        Location(c, CITY_COORDS[c]["latitude"], CITY_COORDS[c]["longitude"])
        for c in cities
        if c in CITY_COORDS
    ]


def poll_once(locations: list[Location]) -> list[Event]:
    """Producer: erzeugt je Stadt ein Live-Event (Fehler werden isoliert)."""
    events: list[Event] = []
    for loc in locations:
        try:
            events.append(fetch_current(loc))
        except Exception as exc:  # ein Stadtfehler darf den Tick nicht stoppen
            print(f"  ! Abruf für {loc.city} fehlgeschlagen: {exc}")
    return events


def ingest(events: list[Event], db_path: Path = DEFAULT_DB_PATH) -> int:
    """Consumer: schreibt Events per Upsert in die Datenbank."""
    frame = events_to_frame(events)
    return save_measurements(frame, db_path, mode="live")


def run_stream(
    cities: list[str],
    interval: float = STREAM_INTERVAL_SECONDS,
    iterations: int | None = None,
    db_path: Path = DEFAULT_DB_PATH,
) -> None:
    """Führt die Streaming-Schleife aus.

    ``iterations=None`` läuft endlos (mit Strg+C abbrechbar), ein
    positiver Wert begrenzt die Anzahl der Ticks.
    """
    locations = _locations(cities)
    if not locations:
        raise SystemExit("Keine gültigen Städte angegeben.")

    print(f"Streaming gestartet [Live (Open-Meteo)] – {len(locations)} Städte, Intervall {interval:.0f}s.")
    tick = 0
    try:
        while iterations is None or tick < iterations:
            tick += 1
            events = poll_once(locations)
            written = ingest(events, db_path)
            total = count_measurements(db_path)
            print(f"  Tick {tick}: {written} Events aufgenommen, Bestand gesamt {total}.")
            if iterations is not None and tick >= iterations:
                break
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStreaming durch Nutzer beendet.")
    print("Streaming beendet.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Live-Streaming-Aufnahme (Open-Meteo)")
    parser.add_argument("--cities", nargs="+", default=["Aalen", "Stuttgart", "Berlin"],
                        help="Liste der Städte (Default: Aalen Stuttgart Berlin)")
    parser.add_argument("--interval", type=float, default=STREAM_INTERVAL_SECONDS,
                        help="Sekunden zwischen den Abrufen")
    parser.add_argument("--iterations", type=int, default=None,
                        help="Anzahl der Ticks (Default: endlos)")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="Pfad zur SQLite-Datei")
    args = parser.parse_args()

    run_stream(
        cities=args.cities,
        interval=args.interval,
        iterations=args.iterations,
        db_path=Path(args.db),
    )


if __name__ == "__main__":
    main()
