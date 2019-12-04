[logo]: https://www.elkem.com/globalassets/foundry/tech-advice/icon_tech-advice_reproducibility-and-consistency.png

![alt text][logo]

# Mapgroup Checks
Prüft diverse Mapgruppen-Filter, d.h. excel files,
auf spezifische Art von Inkonsistenz, Inkompatibilität & Verbesserungsoptionen.

**Stand 4.12.2019** besitzt **Mapgroup Checks** zwei Anwendungen:

* **Bankbasisfilter-Prüfung**
* **Bilanzgliederungsfilter-Prüfung**

### Anleitung
Im Folgenden folgt eine kurze Anleitung zur Ausführung von **Mapgroup Checks**, die
voraussetzt, dass Sie über einen **python interpreter** verfügen, um **Mapgroup Checks**
nutzen zu können:

1. Konvertieren Sie die zu prüfende Datei (= excel file) immer zuerst zu einer .csv-Datei
2. Konfigurieren Sie das jeweilige config file, wenn nötig
3. **Mapgroup Checks** starten mit:
``python -m anwendung.py``

## Erläuterung
Jede Anwendung hat eigene Anforderungen, im Folgenden finden Sie eine Begriffserläuterung zur
leichteren Interpretation der Ergebnisse. Wir unterscheiden zwischen **Quellen**, **Mapgruppen**,
**Merkmalen von Mapgruppen** & **Merkmalsausprägungen von Mapgruppen**, z.B.:

| Quelle | Mapgruppe | Merkmal   | Merkmalsausprägung |   |
|--------|-----------|-----------|--------------------|---|
| "ABS"  | MG01      | KontoNr   | (1, 2, 3)          |   |


Zudem unterscheiden wir zwischen ein-, zwei- und dreistelligen Mapgruppen. Die Stelligkeit einer
Mapgruppe ergibt sich aus der Anzahl der zu dieser Mapgruppe gegebenen Merkmale., d.h. "MG01" ist
einstellig.

### Erläuterung: Bankbasis
Bei der Bankbasisanwendung werden die Daten auf **Inkompatibilität**, **Inkonsistenz** & **Verbesserungsoptionen**
geprüft.

* **INKOMPATIBEL**: Zwei verschiedene Mapgruppen heißen inkompatibel genau dann wenn sie einstellig sind, 
der Schnitt zwischen ihren Merkmalsausprägungen nicht leer ist, aber verschiedene Merkmale gegebenen sind, z.B.:

| Quelle | Mapgruppe | Merkmal   | Merkmalsausprägung |   |
|--------|-----------|-----------|--------------------|---|
| "ABS"  | MG01      | KonNr     | (1, 2, 3)          |   |
| "ABS   | MG02      | KonArCo   | 1                  |   |


* **INKONSISTENT**: Zwei verschiedene Mapgruppen heißen inkonsistent genau dann wenn
sie dieselbe Merkmalsausprägungen & dieselbe Quelle besitzen, z.B.:

| Quelle | Mapgruppe | Merkmal   | Merkmalsausprägung |   |
|--------|-----------|-----------|--------------------|---|
| "ABS"  | MG01      | KonNr     | (1, 2, 3)          |   |
| "ABS   | MG01      | KonNr     | (1, 2, 3)          |   |


* **VERBESSERUNGSPOTENZIAL**: Zwei verschiedene Mapgruppen stellen eine Verbesserungsoption dar genau dann wenn
sie in einander intergiert werden können:

| Quelle | Mapgruppe | Merkmal   | Merkmalsausprägung |   |
|--------|-----------|-----------|--------------------|---|
| "ABS"  | MG01      | KonNr     | (1, 2, 3)          |   |
| "ABS"  | MG01      | SubSy     | 0                  |   |
| "ABS"  | MG02      | KonNr     | (4, 6)             |   |
| "ABS"  | MG02      | SubSy     | 0                  |   |
