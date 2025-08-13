"""
    This module evaluates the primary parameters of the train schedules, both pre- and post-Deutschlandtakt, which are:
    travel time (Reisezeit), the pure travel speed with the train (Befoerderungsgeschwindigkeit), comfort (Komfort),
    and train freuency (Taktfrequenz).

    Parameters concerning transits are ignored, as in this case we evaluate direct transits between two destinations.
"""

from pathlib import Path

from functions import read_all_data, calculation_grundlegend, gewichtung, erschliessungsqualitaet, resultat

#  Testcase
if __name__ == '__main__':
    """
    First Evaluation only for Jahresfahrplan 2025, to check if the code works correct
    Please check the correct data_path in the end if some troubles occur when the file will be read.
    """
    file_name = "Auswertung Fahrplan 2025.xlsx"
    data_path = Path("../../data")
    evaluation = read_all_data(data_path / file_name)
    departures = evaluation.keys()
    erreichbarkeit = pd.DataFrame(columns = ["Erreichbarkeitsindex"], index = list(departures))

    for departure in departures:
        results = calculation_grundlegend(evaluation[departure], schalter = False)
        weighted_idx = gewichtung(results, schalter = False)
        eq_verbindung = erschliessungsqualitaet(weighted_idx)
        erschliessungsindex = resultat(eq_verbindung)
        print(departure)
        print(erschliessungsindex)