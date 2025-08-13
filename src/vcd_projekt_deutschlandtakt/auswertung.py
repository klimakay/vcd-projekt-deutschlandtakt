"""
    This module evaluates the primary parameters of the train schedules, both pre- and post-Deutschlandtakt, which are:
    travel time (Reisezeit), the pure travel speed with the train (Befoerderungsgeschwindigkeit), comfort (Komfort),
    and train freuency (Taktfrequenz).

    data files concerning transits, espacially umsteigezeit and Anzahl Umsteigevorgänge can be taken into account,
     if you switch schalter on True.
"""

from pathlib import Path

import pandas as pd

from functions import read_all_data, calculation_grundlegend, gewichtung, erschliessungsqualitaet, resultat

#  Testcase
if __name__ == '__main__':
    """
    Please check the correct path for in- and output files, so that nothing is overwritten
    that does not belong to the respective data.
    """
    input_file = "Auswertung Fahrplan 2025.xlsx"
    output_file = "Output Fahrplan 2025.xlsx"
    input_data_path = Path("../../data/input")
    output_path = Path("../../data/output")
    evaluation = read_all_data(input_data_path/input_file)
    departures = evaluation.keys()
    erreichbarkeit = pd.DataFrame(columns = ["Erreichbarkeitsindex"], index = list(departures))


    for departure in departures:
        results = calculation_grundlegend(evaluation[departure], schalter = False)
        weighted_idx = gewichtung(results, schalter = False)
        eq_verbindung = erschliessungsqualitaet(weighted_idx)
        erschliessungsindex = resultat(eq_verbindung)
        erreichbarkeit.loc[departure,"Erreichbarkeitsindex"] = erschliessungsindex

    erreichbarkeit.to_excel(output_path/output_file)