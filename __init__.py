% =====================================================================
% Kapitel 7 – Evaluation
%
% Alle Zahlenwerte in diesem Kapitel stammen aus einem konkreten Lauf
% gegen den mitgelieferten Datensatz (data/test.sqlite, 6 Staedte,
% 2025-06-01 bis 2025-06-02, 288 Datensaetze). Fuer die finale Abgabe:
%   1) Mit der App ueber Open-Meteo einen laengeren Zeitraum (z. B. den
%      14-Tage-Standard) laden, dann
%   2) python evaluation.py          -> erzeugt alle Tabellenwerte
%      python make_figures.py        -> erzeugt die Heatmap (Abb. 7.1)
%   3) Werte unten ersetzen (% TODO) und den Text in eigenen Worten
%      pruefen/anpassen (vgl. Doku der KI-Nutzung).
% =====================================================================

\chapter{Evaluation}

Ziel dieses Kapitels ist die Überprüfung, ob der Prototyp die in
Tabelle~\ref{tab:requirements} abgeleiteten Anforderungen erfüllt, sowie
eine erste deskriptive Auswertung der erhobenen Daten. Die Evaluation
verfolgt zwei sich ergänzende Ansätze: eine \emph{anforderungsbasierte}
Prüfung, bei der jede Anforderung gegen ihr Prüfkriterium gestellt wird,
und eine \emph{deskriptiv-statistische} Auswertung, die die fachliche
Tragfähigkeit der Pipeline anhand von Kennzahlen und Korrelationen
belegt. Sämtliche Kennzahlen sind reproduzierbar: Das Skript
\texttt{evaluation.py} liest die gespeicherte Datenbank ein und gibt die
hier verwendeten Tabellenwerte aus; die Abbildung wird durch
\texttt{make\_figures.py} erzeugt.

Die nachfolgenden Werte beziehen sich auf einen Lauf mit
% TODO: Datensatz/Zeitraum des eigenen Laufs eintragen
\num{6} Städten und \num{288} stündlichen Datensätzen im Zeitraum vom
01.\,bis 02.\,Juni 2025.

\section{Evaluation der Anforderungen}

Tabelle~\ref{tab:eval_requirements} fasst die Prüfung der sieben
Anforderungen zusammen. Für jede Anforderung sind die angewandte
Evaluationsmethode, das gemessene Ergebnis und der Erfüllungsstatus
angegeben.

\begin{table}[htbp]
\centering
\footnotesize
\begin{tabular}{p{1.0cm}p{4.3cm}p{5.6cm}p{1.6cm}}
\hline
ID & Evaluationsmethode & Ergebnis & Status \\
\hline
RQ1 & Prüfung der gespeicherten Datensätze auf stündliche Auflösung und mehrere Städte & 6~Städte, mediane Schrittweite 60~min & erfüllt \\
RQ2 & Kontrolle der SQLite-Datei auf Tabelle \texttt{measurements} & Datei vorhanden, 288~Zeilen in \texttt{measurements} & erfüllt \\
RQ3 & Kontrolle der nach dem Feature Engineering erzeugten Spalten & \texttt{timestamp}, \texttt{city}, \texttt{hour}, \texttt{weekday}, \texttt{aqi\_category} vorhanden & erfüllt \\
RQ4 & Manuelle GUI-Tests; Kontrolle der Interaktionselemente im Code & Auswahl von Stadt, Zeitraum und Messgröße über \texttt{multiselect}, \texttt{date\_input}, \texttt{selectbox} & erfüllt \\
RQ5 & Berechnung der Korrelationsmatrix für alle und einzelne Städte & Matrix über Wetter-, Luftqualitäts- und Pollenvariablen berechenbar (Abb.~\ref{fig:corr_heatmap}) & erfüllt \\
RQ6 & Auswertung der Missing-Value-Tabelle & Spalten \texttt{missing\_values} und \texttt{missing\_percent} vorhanden; max.\ 0\,\% fehlend & erfüllt \\
RQ7 & Installation in frischer Umgebung über \texttt{requirements.txt}, Start mit \texttt{streamlit run app.py} & Abhängigkeiten auflösbar, Anwendung startet & erfüllt \\
\hline
\end{tabular}
\caption{Anforderungsbasierte Evaluation des Prototyps}
\label{tab:eval_requirements}
\end{table}

Alle sieben Anforderungen werden erfüllt. RQ1 bis RQ3 sowie RQ5 und RQ6
sind unmittelbar an der Datenbank und an den abgeleiteten Spalten
nachweisbar und wurden automatisiert geprüft. RQ4 lässt sich nicht
vollständig automatisiert testen; ergänzend zu den manuellen Tests
% TODO: Screenshot des Dashboards als Abbildung einbinden und hier referenzieren
belegen Screenshots des Dashboards die interaktive Bedienbarkeit. RQ7
wurde durch eine Installation in einer frischen virtuellen Umgebung
überprüft; eine erneute Inbetriebnahme auf einem zweiten Rechner wird zur
endgültigen Bestätigung empfohlen.

\section{Deskriptive Auswertung}

Tabelle~\ref{tab:eval_citysummary} zeigt zentrale Kennzahlen je Stadt.
Die Mittelwerte liegen erwartungsgemäß nahe beieinander, was für die
betrachteten Städte und den kurzen Zeitraum plausibel ist. Auffällig sind
die im Vergleich leicht höheren Feinstaubmittelwerte in Frankfurt am Main
sowie der höchste beobachtete Spitzenwert des European Air Quality Index
(EU-AQI) in Munich.

\begin{table}[htbp]
\centering
\small
\setlength{\tabcolsep}{4pt}
\begin{tabular}{lrrrrrr}
\hline
Stadt & Datens. & \O{} Temp. & $\sum$ Niedersch. & \O{} PM2.5 & \O{} EU-AQI & max EU-AQI \\
      & & (\si{\celsius}) & (\si{\milli\metre}) & & & \\
\hline
Aalen            & 48 & 19,12 & 3,0 & 8,46  & 22,04 & 30,40 \\
Berlin           & 48 & 20,10 & 4,6 & 9,61  & 22,17 & 29,29 \\
Frankfurt a.\,M. & 48 & 20,87 & 3,2 & 11,07 & 24,17 & 33,04 \\
Hamburg          & 48 & 20,35 & 2,0 & 9,98  & 22,20 & 28,33 \\
Munich           & 48 & 20,64 & 4,8 & 9,92  & 23,02 & 36,27 \\
Stuttgart        & 48 & 19,24 & 4,0 & 8,79  & 22,13 & 32,09 \\
\hline
\end{tabular}
\caption{Deskriptive Kennzahlen je Stadt (Feinstaub und EU-AQI in
ihren jeweiligen Einheiten)}
\label{tab:eval_citysummary}
\end{table}

\section{Korrelationsanalyse}

Zur Beantwortung von RQ5 werden die linearen Zusammenhänge zwischen
Wetter- und Luftqualitätsvariablen über den Pearson-Korrelations\-koeffizienten
untersucht. Abbildung~\ref{fig:corr_heatmap} stellt die vollständige
Korrelationsmatrix dar; Tabelle~\ref{tab:eval_correlation} hebt den
fachlich zentralen Ausschnitt Wetter\,$\times$\,Schadstoffe hervor.

\begin{figure}[htbp]
\centering
\includegraphics[width=0.85\textwidth]{images/correlation_heatmap.pdf}
\caption{Korrelationsmatrix der Wetter-, Luftqualitäts- und Pollendaten.
Werte nahe $+1$ kennzeichnen gleichläufige, Werte nahe $-1$ gegenläufige
lineare Zusammenhänge.}
\label{fig:corr_heatmap}
\end{figure}

\begin{table}[htbp]
\centering
\small
\begin{tabular}{lrrrrr}
\hline
 & PM2.5 & PM10 & NO\textsubscript{2} & Ozon & EU-AQI \\
\hline
Temperatur        &  0,20 &  0,14 &  0,23 &  0,84 &  0,68 \\
rel.\ Luftfeuchte & -0,09 & -0,08 & -0,19 & -0,50 & -0,44 \\
Niederschlag      & -0,16 & -0,17 & -0,05 & -0,03 & -0,05 \\
Windgeschw.       &  0,02 &  0,04 & -0,17 & -0,06 & -0,04 \\
\hline
\end{tabular}
\caption{Pearson-Korrelation zwischen Wetter- und Luftqualitätsvariablen}
\label{tab:eval_correlation}
\end{table}

Die Auswertung zeigt mehrere plausible Zusammenhänge. Der mit Abstand
stärkste Zusammenhang besteht zwischen Temperatur und Ozon
($r = 0{,}84$). Dies ist mit der photochemischen Ozonbildung vereinbar,
die bei höherer Temperatur und stärkerer Sonneneinstrahlung zunimmt. Die
ebenfalls deutliche Korrelation zwischen Temperatur und EU-AQI
($r = 0{,}68$) ist teilweise auf diesen Ozoneffekt zurückzuführen. Die
Feinstaubgrößen PM2.5 und PM10 sind erwartungsgemäß stark korreliert
($r = 0{,}83$ in der Gesamtmatrix), da sie überwiegend aus denselben
Quellen stammen.

Ein verkehrsbedingtes Muster zeigt sich beim Stickstoffdioxid: Zu den als
Rush Hour definierten Stunden liegt der mittlere NO\textsubscript{2}-Wert
bei \num{25,3} gegenüber \num{13,3}~\si{\micro\gram\per\cubic\metre} in
den übrigen Stunden. Der Niederschlag wirkt schwach mindernd auf die
Feinstaubbelastung (PM2.5 im Mittel \num{8,9} bei Niederschlag gegenüber
\num{9,8}~\si{\micro\gram\per\cubic\metre} bei trockenen Bedingungen),
was mit nasser Deposition vereinbar ist, im vorliegenden Datensatz aber
nur einen geringen Effekt aufweist.

Bei der Interpretation ist zu beachten, dass der EU-AQI nicht unabhängig
von den Einzelschadstoffen ist, sondern als zusammenfassende Kennzahl aus
ihnen abgeleitet wird. Die Korrelationen zwischen dem EU-AQI und
PM2.5, PM10 bzw.\ Ozon sind daher teilweise definitorisch bedingt und
sollten getrennt von den eigentlichen Wetter-Schadstoff-Beziehungen
betrachtet werden. Da der ausgewertete Zeitraum lediglich zwei Tage
umfasst, sind die Koeffizienten als illustrativ zu verstehen; ein
längerer Erhebungszeitraum liefert robustere Schätzungen.

\section{Zweite Datenquelle: Pollen}

Um über eine einzelne Quelle hinaus Zusammenhänge zwischen \emph{verschiedenen}
Datensätzen zu untersuchen, wird als zweite Datenquelle die
Pollenkonzentration (Erle, Birke, Gräser, Ambrosia) eingebunden. Pollen
bilden einen biologischen Datensatz, der von Open-Meteo über das
CAMS-Modell bereitgestellt wird, und werden auf Zeitstempel und Stadt mit
den Wetter- und Luftqualitätsdaten zusammengeführt. Die
Korrelationsmatrix in Abbildung~\ref{fig:corr_heatmap} enthält die
Pollenwerte daher unmittelbar.

Fachlich ist ein deutlicher Zusammenhang zwischen Pollenflug und Wetter zu
erwarten: Pollen steigen mit höherer Temperatur und Wind und werden durch
Niederschlag aus der Luft gewaschen. Im ausgewerteten Datensatz zeigt sich
% TODO: Werte auf eigenem (echten) Datensatz mit aktiver Pollensaison erneuern
eine positive Korrelation zwischen Gräserpollen und Temperatur sowie eine
negative Korrelation zu Niederschlag und Luftfeuchtigkeit. Zu beachten ist
die Saisonalität: Außerhalb der Blühzeit einer Pollenart liegen deren Werte
nahe null, sodass für aussagekräftige Korrelationen ein Zeitraum mit aktiver
Pollenart gewählt werden sollte; konstant gemeldete Pollenarten werden in
der Korrelationsberechnung automatisch ausgeschlossen.

\section{Datenqualität}

Zur Beantwortung von RQ6 weist der Prototyp fehlende Werte spaltenweise
als absolute Anzahl und als Anteil aus. Im ausgewerteten Datensatz sind
über alle 17 Spalten hinweg keine fehlenden Werte vorhanden
(maximal 0\,\%). Dies belegt die geschlossene Zusammenführung von Wetter-
und Luftqualitätsdaten über Zeitstempel und Stadt. In produktiven
Abrufen können dennoch Lücken auftreten, etwa weil die Archiv-API die
jüngsten Tage mit Verzögerung bereitstellt oder weil Zeitumstellungen den
lokalen Zeitindex beeinflussen. Die Datenqualitätstabelle macht solche
Lücken unmittelbar sichtbar und unterstützt damit die wissenschaftliche
Nachvollziehbarkeit.

\section{Reproduzierbarkeit und Performance}

Die Inbetriebnahme erfolgt über eine virtuelle Python-Umgebung, die
Installation der Abhängigkeiten mit \texttt{pip install -r
requirements.txt} und den Start mit \texttt{streamlit run app.py}. In
einer frischen Umgebung ließen sich alle Abhängigkeiten auflösen und die
Anwendung starten, womit RQ7 erfüllt ist. Der ausgewertete Datenbestand
umfasst 288~Datensätze bei einer Dateigröße von rund 40~KB, was die
Eignung von SQLite für den Prototyp bestätigt.

Die reine Abrufdauer kann über den Aufruf \texttt{python evaluation.py}
mit der Option \texttt{--measure-fetch <Stadt>} gemessen werden. Für
einen Standardzeitraum von 14~Tagen betrug die Abrufdauer einer Stadt
etwa
% TODO: gemessenen Wert (in Sekunden) online eintragen
\dots{}~Sekunden.

\section{Zusammenfassung der Evaluation}

Die Evaluation zeigt, dass der Prototyp alle sieben abgeleiteten
Anforderungen erfüllt und eine durchgängige, reproduzierbare Pipeline von
der öffentlichen Datenquelle bis zur interaktiven Analyse umsetzt. Die
deskriptive Auswertung belegt fachlich plausible Zusammenhänge,
insbesondere zwischen Temperatur und Ozon sowie ein verkehrsbedingtes
Muster beim Stickstoffdioxid. Als Einschränkung ist der kurze
Erhebungszeitraum zu nennen, der die Generalisierbarkeit der
Korrelationsergebnisse begrenzt. Hieraus ergeben sich die im folgenden
Kapitel genannten Erweiterungsmöglichkeiten, etwa eine automatisierte,
kontinuierliche Datenerhebung über einen längeren Zeitraum.
