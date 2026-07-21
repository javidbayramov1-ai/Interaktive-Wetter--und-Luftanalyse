# Weather & Air Quality Analytics Dashboard

Lauffähiger Prototyp einer interaktiven Applikation zur **Visualisierung und
Analyse von Wetter- und Luftqualitätsdaten** deutscher Städte. Das Projekt
deckt eine durchgängige Datenpipeline ab: Datenbeschaffung (Batch **und**
Streaming), Speicherung, Aufbereitung, Visualisierung und Korrelationsanalyse.

## Überblick

| Schritt | Umsetzung |
|---|---|
| Datenquelle | Open-Meteo (Wetter- und Luftqualitäts-API, ohne API-Schlüssel) |
| Beschaffung – Batch | Historische Stundenwerte über die Archiv-API (`src/open_meteo.py`) |
| Zweite Datenquelle | Pollendaten (Erle, Birke, Gräser, Ambrosia) über die CAMS-API (`src/pollen.py`) |
| Beschaffung – Streaming | Fortlaufende Aufnahme aktueller Werte (`src/streaming.py`, `src/live_client.py`) |
| Speicherung | SQLite mit Upsert und Primärschlüssel (`src/storage.py`) |
| Aufbereitung | Feature Engineering und Datenqualität (`src/features.py`) |
| Analyse | Kennzahlen, Korrelationen, Tagesprofile (`src/analysis.py`) |
| Visualisierung | Interaktives Dashboard (`app.py`) |
| Evaluation | Anforderungsbasierte Auswertung mit echten Zahlen (`evaluation.py`) |

## Installation

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Ausführen

### 1. Dashboard (Batch)

```bash
streamlit run app.py
```

Im Browser Städte und Zeitraum wählen und auf **Daten laden und speichern**
klicken. Hierfür ist eine Internetverbindung nötig; einmal geladene Daten
bleiben anschließend in der lokalen Datenbank gespeichert.

### 2. Streaming-Producer

Schreibt fortlaufend aktuelle Messwerte in dieselbe Datenbank, die das
Dashboard liest:

```bash
python -m src.streaming --cities Aalen Berlin --interval 300
```

Anschließend im Dashboard im Reiter **Live-Streaming** auf *Aktualisieren*.

### 3. Tests

```bash
python -m pytest -q
```

### 4. Evaluation und Abbildung (für den Bericht)

```bash
python evaluation.py            # Kennzahlen, Anforderungs-Check, Korrelationen
python make_figures.py          # erzeugt latex/images/correlation_heatmap.pdf
```

## Projektstruktur

```text
config.py                  Zentrale Konfiguration (Variablen, Pfade, Intervalle)
app.py                     Streamlit-Dashboard (Analyse + Live-Reiter)
evaluation.py              Anforderungsbasierte Evaluation mit Kennzahlen
make_figures.py            Erzeugung der Korrelations-Heatmap
src/
  open_meteo.py            Batch-Client (Archiv-API), mit Retry und Fehlerisolierung
  pollen.py                Zweite Datenquelle: Pollendaten (CAMS)
  live_client.py           Live-Client (Current-API) für Streaming
  streaming.py             Producer/Consumer und CLI der Streaming-Schicht
  storage.py               SQLite-Persistenz mit Upsert (Primärschlüssel)
  features.py              Feature Engineering und Datenqualität
  analysis.py              Kennzahlen, Korrelationen, Tagesprofile, Ausreißer
  city_catalog.py          Städtekatalog mit Koordinaten
tests/                     Pytest-Suite der Datenpipeline
docs/                      Berichtshilfen (Anforderungen, Gliederung, Architektur)
latex/                     LaTeX-Ausarbeitung (inkl. Kapitel 7 Evaluation)
```

## Architektur

Siehe `docs/architecture.mmd`. Kurzform:

```
Batch:      Archiv-API  -> Batch-Client ---\
                                            +-> SQLite (Upsert) -> Features -> Analyse/Dashboard
Streaming:  Current-API -> Producer -> Consumer -/
```

## Ausbaustufen des Streamings

Die mitgelieferte Streaming-Schicht ist bewusst infrastrukturfrei (reines
Python, Polling). Sie lässt sich bei Bedarf zu einer klassischen
Streaming-Architektur ausbauen:

1. **Aktuell:** Producer pollt die Current-API, Consumer schreibt per Upsert
   in SQLite (Micro-Batch).
2. **Mittel:** Message-Broker (Apache Kafka, Redpanda oder MQTT) zwischen
   Producer und Consumer; Entkopplung und Pufferung.
3. **Voll:** Kafka → Apache Spark Structured Streaming → Zeitreihen-Datenbank
   (TimescaleDB/InfluxDB) → Dashboard/Grafana.

## Datenquelle und Lizenz

Daten von [Open-Meteo](https://open-meteo.com/) (frei für nicht-kommerzielle
Nutzung, ohne API-Schlüssel). Wetterdaten über die Archiv-/Forecast-API,
Luftqualitätsdaten über die Air-Quality-API. Als zweite Datenquelle werden
Pollendaten (CAMS, nur Europa) über die Air-Quality-API abgerufen und mit
Wetter und Luftqualität korreliert (Pollenflug steigt mit Wärme/Wind, sinkt
bei Regen). Pollen sind saisonal: für aussagekräftige Korrelationen einen
Zeitraum mit aktiver Pollenart wählen.

## Hinweis zur KI-Nutzung

Generative KI wurde unterstützend genutzt; die Verantwortung für Korrektheit,
Code und finalen Text liegt beim Autor. Details in
`docs/ai_usage_documentation.md`.
