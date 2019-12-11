[logo]: https://www.elkem.com/globalassets/foundry/tech-advice/icon_tech-advice_reproducibility-and-consistency.png

![alt text][logo]

# Mapgroup Checks
Prüft diverse Mapgruppen-Filter, d.h. excel files,
auf spezifische Art von Inkonsistenz, Inkompatibilität & Verbesserungsoptionen.

**Stand 9.12.2019** besitzt **Mapgroup Checks** zwei Anwendungen:

* **Bankbasisfilter-Prüfung**
* **Bilanzgliederungsfilter-Prüfung**

### Anleitung
Im Folgenden folgt eine kurze Anleitung zur Ausführung von **Mapgroup Checks**, die
voraussetzt, dass Sie über einen **python interpreter** verfügen, um **Mapgroup Checks**
nutzen zu können:

0. Installieren Sie **einmalig** alle nötigen Pakete aus package_installer mit: ``python install.py``
1. Konvertieren Sie die zu prüfende Datei (= excel file) immer zuerst zu einer .csv-Datei
2. Konfigurieren Sie das jeweilige config file, **wenn nötig**
3. **Mapgroup Checks** ausführen mit: ``python bbs.py`` oder ``python bg.py``
