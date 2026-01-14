\# ParkAPI - Python Desktop Client



Ein moderner Desktop-Client zur Verwaltung von Parkplatzdaten. Diese Anwendung kommuniziert mit einem \*\*C# ASP.NET Core Backend\*\*, welches die Daten über \*\*Apache Kafka\*\* verarbeitet und speichert.



\## System-Architektur



Die Anwendung folgt einer klassischen Client-Server-Struktur:



1\.  \*\*Client (Python):\*\* Grafische Benutzeroberfläche mit `CustomTkinter`.

2\.  \*\*Backend (C#):\*\* REST-API Controller, die Anfragen entgegennehmen.

3\.  \*\*Infrastruktur (Docker):\*\* Das Backend und Kafka laufen in Containern.

4\.  \*\*Datenbank (Kafka):\*\* Event-Streaming Plattform zur persistenten Speicherung.







---



\## Features



\* \*\*Echtzeit-Abfrage:\*\* Lädt alle Parkplätze aus dem System.

\* \*\*ID-Suche:\*\* Gezielte Informationen zu einem bestimmten Parkplatz abrufen.

\* \*\*Admin-Dashboard:\*\* Neue Parkplätze anlegen inklusive:

&nbsp;   \* Name des Parkplatzes

&nbsp;   \* Ort/Stadt (Location)

&nbsp;   \* Maximale Kapazität (Anzahl Plätze)

\* \*\*Fehler-Handling:\*\* Integrierte Prüfung auf Verbindungsfehler und API-Statuscodes.



---



\## Installation \& Setup



\### Voraussetzungen

\* Installiertes \*\*Python 3.10+\*\*

\* Das C# Backend muss gestartet sein (Docker-Container aktiv)



\### 1. Bibliotheken installieren

Öffne dein Terminal (oder CMD) und installiere die notwendigen Abhängigkeiten:



pip install customtkinter requests

