"""Erzeugt die Korrelations-Heatmap als Vektor-PDF für Kapitel 7.

    python make_figures.py [--db pfad/zur.sqlite]

Legt die Datei latex/images/correlation_heatmap.pdf an.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from src.analysis import correlation_matrix
from src.features import enrich
from src.storage import DEFAULT_DB_PATH, load_measurements

LABELS = {
    "temperature_2m": "Temp.",
    "relative_humidity_2m": "Luftf.",
    "precipitation": "Niedersch.",
    "wind_speed_10m": "Wind",
    "pm10": "PM10",
    "pm2_5": "PM2.5",
    "nitrogen_dioxide": "NO2",
    "ozone": "Ozon",
    "european_aqi": "EU-AQI",
    "alder_pollen": "Erle",
    "birch_pollen": "Birke",
    "grass_pollen": "Gräser",
    "ragweed_pollen": "Ambrosia",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=None)
    parser.add_argument("--out", default="latex/images/correlation_heatmap.pdf")
    args = parser.parse_args()

    db_path = Path(args.db) if args.db else DEFAULT_DB_PATH
    df = enrich(load_measurements(db_path))
    cor = correlation_matrix(df)
    if cor.empty:
        raise SystemExit("Keine Korrelationsmatrix berechenbar – zuerst Daten laden.")

    names = [LABELS.get(c, c) for c in cor.columns]
    data = cor.to_numpy()

    fig, ax = plt.subplots(figsize=(7.0, 6.0))
    im = ax.imshow(data, cmap="RdBu_r", vmin=-1, vmax=1)

    ax.set_xticks(range(len(names)), labels=names, rotation=45, ha="right", fontsize=9)
    ax.set_yticks(range(len(names)), labels=names, fontsize=9)

    for i in range(len(names)):
        for j in range(len(names)):
            val = data[i, j]
            ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    color="white" if abs(val) > 0.55 else "black", fontsize=8)

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Pearson-Korrelationskoeffizient r", fontsize=9)
    ax.set_title("Korrelation: Wetter-, Luftqualitäts- und Pollendaten", fontsize=11)
    fig.tight_layout()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight")
    print(f"Abbildung gespeichert: {out}  (Quelle: {db_path})")


if __name__ == "__main__":
    main()
