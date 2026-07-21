\documentclass[oneside]{ausarbeitung}
\bibliography{latexlit}

\begin{document}
\selectlanguage{ngerman}
\Projektbericht
\DataScience

\title{Entwicklung eines interaktiven Dashboards zur Analyse von Wetter- und Luftqualitätsdaten}
\author{Javid Bayramov}
\matrikelnr{Matrikelnummer eintragen}
\examinerIsAProfessortrue
\examinerA{Prof.~Dr.~Gregor~Grambow}
\date{Abgabedatum eintragen}

\maketitle
\cleardoublepage
\pagenumbering{roman}
\setcounter{page}{1}
\makeaffirmation
\cleardoublepage

\begin{abstract}
Diese Projektarbeit behandelt die Entwicklung eines Prototyps zur Visualisierung und Analyse von Wetter- und Luftqualitätsdaten. Die Anwendung ruft öffentliche Datenquellen über APIs ab, speichert die Daten lokal in einer SQLite-Datenbank, bereitet sie mit Python auf und stellt sie in einem interaktiven Streamlit-Dashboard dar. Zusätzlich werden Datenqualität und lineare Zusammenhänge zwischen Wetter- und Luftqualitätsvariablen analysiert.
\end{abstract}

\cleardoublepage
\tableofcontents
\listoffigures
\listoftables
\lstlistoflistings

\cleardoublepage
\pagenumbering{arabic}
\setcounter{page}{1}

\chapter{Einleitung}
\section{Motivation}
Wetter- und Luftqualitätsdaten werden von öffentlichen Stellen und offenen Datenplattformen kontinuierlich bereitgestellt. Für eine datengetriebene Auswertung müssen solche Rohdaten jedoch zunächst beschafft, gespeichert, aufbereitet und verständlich visualisiert werden. Daraus ergibt sich der Bedarf an einer reproduzierbaren Datenapplikation, die mehrere Datenquellen zusammenführt und explorative Analysen ermöglicht.

\section{Problemstellung und Abgrenzung}
Die Arbeit betrachtet die Entwicklung eines Prototyps für eine interaktive Analyseanwendung. Nicht betrachtet werden eine produktive Cloud-Bereitstellung, medizinische Bewertungen von Luftqualität oder eine Machine-Learning-basierte Vorhersage.

\section{Ziel der Arbeit}
Ziel ist die Entwicklung eines lauffähigen Prototyps, der Wetter- und Luftqualitätsdaten öffentlicher APIs abruft, in SQLite speichert, aufbereitet, visualisiert und durch Korrelationsanalysen auswertet.

\section{Vorgehen}
Die Arbeit folgt den Schritten Grundlagen, Problemanalyse, Konzept, Implementierung, Inbetriebnahme und Evaluation.

\chapter{Grundlagen}
\section{Öffentliche APIs}
\section{Zeitreihendaten}
\section{SQLite}
\section{Pandas}
\section{Streamlit}
\section{Korrelationsanalyse}

\chapter{Problemanalyse}
\section{Anforderungen}
\begin{table}[htbp]
\centering
\begin{tabular}{p{1.6cm}p{4cm}p{7cm}}
\hline
ID & Titel & Beschreibung \\
\hline
RQ1 & Public Data Acquisition & Die Anwendung muss öffentliche Wetter- und Luftqualitätsdaten für auswählbare Städte abrufen können. \\
RQ2 & Persistent Storage & Die abgerufenen Daten müssen lokal gespeichert werden. \\
RQ3 & Data Preparation & Die Daten müssen in ein einheitliches tabellarisches Format überführt und mit Zusatzmerkmalen ergänzt werden. \\
RQ4 & Interactive Visualization & Die Anwendung muss interaktive Visualisierungen für Zeitverläufe und Stadtvergleiche bereitstellen. \\
RQ5 & Correlation Analysis & Die Anwendung muss lineare Zusammenhänge zwischen Wetter- und Luftqualitätsvariablen analysieren. \\
RQ6 & Data Quality Transparency & Die Anwendung muss fehlende Werte transparent darstellen. \\
RQ7 & Reproducible Commissioning & Die Anwendung muss mit dokumentierten Schritten auf einem anderen Rechner ausführbar sein. \\
\hline
\end{tabular}
\caption{Abgeleitete Anforderungen an den Prototyp}
\label{tab:requirements}
\end{table}

\chapter{Konzept}
\section{Architektur}
Die Anwendung besteht aus API-Client, Persistenzschicht, Datenaufbereitung, Analysemodul und Streamlit-Benutzeroberfläche.

\section{Datenfluss}
API-Abruf, JSON-Transformation, Zusammenführung nach Stadt und Zeitstempel, Speicherung in SQLite, Feature Engineering, Analyse und Visualisierung.

\section{Technologieauswahl}
Python, Pandas, SQLite, Streamlit und Plotly werden genutzt, da sie eine schnelle und nachvollziehbare Entwicklung einer Data-Science-Applikation ermöglichen.

\chapter{Implementierung}
\section{API-Anbindung}
\section{Speicherung}
\section{Datenaufbereitung}
\section{Visualisierung}
\section{Korrelationsanalyse}

\chapter{Inbetriebnahme}
Die Anwendung wird über eine virtuelle Python-Umgebung installiert. Danach werden die Abhängigkeiten mit \texttt{pip install -r requirements.txt} installiert und die Anwendung mit \texttt{streamlit run app.py} gestartet.

\chapter{Evaluation}
\section{Evaluation der Anforderungen}
Jede Anforderung aus Tabelle~\ref{tab:requirements} wird geprüft. Dazu werden API-Abruf, Datenbankdatei, erzeugte Spalten, GUI-Funktionen, Korrelationsmatrix, Datenqualitätstabelle und Reproduzierbarkeit der Installation betrachtet.

\chapter{Fazit und Ausblick}
Der entwickelte Prototyp zeigt eine vollständige Pipeline von öffentlicher Datenquelle bis zur interaktiven Analyse. Mögliche Erweiterungen sind zusätzliche Datenquellen, automatisierte Aktualisierung, Deployment und ML-basierte Prognosen.

\printbibliography
\end{document}
