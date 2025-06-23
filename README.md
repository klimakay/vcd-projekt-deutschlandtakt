# VCD Projekt Deutschlandtakt
Dieses Repository enthält ein Modell, sowie zugehörige Daten zur Auswertung der Erreichbarkeit von Bahnhöfen im [Deutschlandtakt](https://www.deutschlandtakt.de/) in der Region Hannover.
Hierfür werden Daten aus dem [Jahresfahrplan 2025](https://bahn.expert/), dem [Zielfahrplan Deutschlandtakt](https://assets.ctfassets.net/scbs508bajse/6wYikPsl1G47nWJw5MHEhn/a0dbf1f255f2cfd6bf033941280da2ba/Netzgrafik_3._Entwurf_Nord.pdf) des
Bundesministeriums für Verkehr sowie des [SPNV Konzept 2040+](https://www.lnvg.de/fileadmin/media/lnvg/SPNV_2019/SPNV_Konzept_2030/LNVG_SPNV-KONZEPT_2030__2040.pdf) 
der Landesnahverkehrsgesellschaft Niedersachsen (LNVG) verwendet, welche als Excel-Dateien vorliegen.  
Die Fahrplandaten sind dort Betriebsstellen bzw. Bahnhöfen im Großraum Hannover zugeordnet.
Die Methodik zur Auswertung basiert dabei auf dem Erreichbarkeitsmodell von Stephan Bunge:  
**Bunge, Stephan, 2011. Analyse und Bewertung der regionalen Erschließungsqualität im Schienenpersonenfernverkehr. Diss. TU Berlin.**  
Das von Bunge verwendete Modell wurde dabei adaptiert und auf den Schienenpersonennahverkehr angewendet.
Das Modell gibt als Auswertung der Input Dateien für jeden untersuchten Ort jeweils eine Zahl aus, welche als Indikatorgröße die Erreichbarkeit eines Ortes im jeweiligen Fahrplan quantifizierbar macht.
Die Ergebnisse werden am Ende wieder als Excel-Datei für den jeweiligen Fahrplan ausgegeben.  
Konkrete Ergebnisse, weitere Datenquellen sowie die gesammelte Methodik des Modells werden später vom [Verkehrsclub Deutschland (VCD) Landesverband Niedersachsen](https://niedersachsen.vcd.org/) als Publikation veröffentlicht.

## Installation
```bash
git clone https://github.com/klimakay/vcd-projekt-deutschlandtakt.git
cd vcd_projekt_deutschlandtakt
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt   # requirements.txt contains: pygame
```