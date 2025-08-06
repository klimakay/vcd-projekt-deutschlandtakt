"""
    All functions are stored here that are used to read data, evaluate the general parameters (step 1), and the
    reachability index (step 2). The variable L_SCHALTER can be used to switch on the model mode for
    data with transfer connections. The corresponding data must be listed in the Excel table as described in the
     code.
"""


from pathlib import Path

import pandas as pd
from pandas import DataFrame, Series

COL_DESTINATION = 'Verbindung nach'
L_SCHALTER = True


def read_all_data(file_path: Path) -> dict[str, DataFrame] | None:
    """
    Reads the input of a .xlsx file containing the evaluation of each connection. Outputs the entire .xlsx file,
    as well as the name of each sheet, which indicates the departure station.


    :param file_path: path and name of the .xlsx evaluation file
    :return: Entire Excel sheet (data) in file_path
    :raise: ValueError if file_path is not a .xlsx file.
    """

    if file_path.suffix == ".xlsx":
        data = pd.read_excel(file_path, sheet_name=None)
        return data

    if file_path.suffix != ".xlsx":
        raise ValueError("The input must be a .xlsx file")
    return None


def calculation_grundlegend(schedule_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calulates all basic parameters for evaluation: Reisezeit (ra),
    Beförderungsgeschwindigkeit (bg), Komfort (as) and Taktfrequenz (zv).

    :param schedule_data: The entire schedule Excel sheet.
    :return: basic_params: a pd.DataFrame including all basic parameters to be calculated.
    """

    def reisezeit(zeit_bahn: pd.DataFrame, zeit_auto: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates the ratio between travel time by train and by car. Output is the ratio in percent.

        :param zeit_bahn: The time it takes to reach the destination by train in min.
        :param zeit_auto: The time it takes to reach the destination by car in min.
        :return: Reisezeit (ra) in %
        """

        return round(zeit_auto/zeit_bahn, 2)


    def befoerderungsgeschwindigkeit(strecke_bahn: pd.DataFrame, zeit_bahn: pd.DataFrame,
                                     umsteigezeit: pd.DataFrame | float | None=None) -> pd.DataFrame:
        """
        Calculate the pure travel speed with the distance traveled and the pure travel time with the train.

        :param strecke_bahn: Distance traveled by train in km.
        :param zeit_bahn: Time traveled by train in min.
        :param umsteigezeit: Time for transit in minute. Note that it is 0 by default, for cases when no transits are
        necessary.
        :return: travel speed in km/h
        """
        if L_SCHALTER is False:
            umsteigezeit = 0


        return round(strecke_bahn / (zeit_bahn - umsteigezeit), 2)
    if L_SCHALTER:
        def umsteigezwang(strecke_bahn: pd.DataFrame, anzahl_umsteigevorgang:pd.DataFrame) -> pd.DataFrame:
            """
            Calculates the ratio of transits along distance traveled by train.

            :param strecke_bahn: Distance traveled by train in km.
            :param anzahl_umsteigevorgang: Number of transits.
            :return: Umsteigezwang (%/km)
            """

            return round(anzahl_umsteigevorgang * 100 / strecke_bahn, 2)

        def umsteigezeit_ratio(zeit_bahn: pd.DataFrame, umsteigezeit: pd.DataFrame) -> pd.DataFrame:
            """
            Calculates the ratio of zeit between transits and the actual travel time.

            :param zeit_bahn: Time traveled by train in min.
            :param umsteigezeit: Time for transit in minute.
            :return: Umsteigezeit (min).
            """

            return round(umsteigezeit / zeit_bahn * 100, 2)


    def komfort(strecke_bahn: pd.DataFrame, strecke_auto: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates the comfort index by dividing the distance traveled by train in km with the distance traveled
        by car in km.

        :param strecke_bahn: Distance traveled by train in km.
        :param strecke_auto: Distance traveled by car in km.
        :return: Komfort (%)
        """

        return round(strecke_bahn / strecke_auto, 2)


    def takt(taktfrequenz: pd.DataFrame) -> pd.DataFrame:
        """
        Gives back the number of trains per hour (taktfrequenz)
        :param taktfrequenz: number of trains/hour
        :return: taktfrequenz (number of trains/hour)
        """
        return round(taktfrequenz,2)


    data = schedule_data
    cols = data.columns
    destination = data[COL_DESTINATION]
    t_bahn = data[cols[1]]
    t_auto = data[cols[2]]
    s_bahn = data[cols[3]]
    s_auto = data[cols[4]]
    taktfrequenz = data[cols[5]]
    if L_SCHALTER:
        t_u = data[cols[6]]
        U = data[cols[7]]



    if L_SCHALTER:
        ra = reisezeit(zeit_bahn=t_bahn, zeit_auto=t_auto)
        bg = befoerderungsgeschwindigkeit(strecke_bahn=s_bahn, zeit_bahn=t_bahn, umsteigezeit=t_u)
        ks = komfort(strecke_bahn=s_bahn, strecke_auto=s_auto)
        zv = takt(taktfrequenz)
        ua = umsteigezeit_ratio(zeit_bahn=t_bahn, umsteigezeit=t_u)
        uv = umsteigezwang(strecke_bahn=s_bahn, anzahl_umsteigevorgang=U)
    else:
        ra = reisezeit(zeit_bahn=t_bahn, zeit_auto=t_auto)
        bg = befoerderungsgeschwindigkeit(strecke_bahn=s_bahn, zeit_bahn=t_bahn)
        ks = komfort(strecke_bahn=s_bahn, strecke_auto=s_auto)
        zv = takt(taktfrequenz)

    if L_SCHALTER:
        basic_params = pd.DataFrame({"Ziel": destination,
                                     "Reisezeit Verhältnis": ra,
                                     "Beförderungsgeschwindigkeit": bg,
                                     "Komfort": ks,
                                     "Taktfrequenz": zv,
                                     "Umsteigezeitverhältnis": ua,
                                     "Umsteigezwang": uv})

        return basic_params
    else:
        basic_params = pd.DataFrame({"Ziel": destination,
                                     "Reisezeit Verhältnis": ra,
                                     "Beförderungsgeschwindigkeit": bg,
                                     "Komfort": ks,
                                     "Taktfrequenz": zv})

        return basic_params


def gewichtung(primary_idx: pd.DataFrame) -> Series | DataFrame:
    """
    Calculates a weighted, relative index for time-dependent and distance-independent input variables to make them
    dimensionally homogeneous.
    :param primary_idx: weighted index
    :return: weighted index for time-dependent and distance-independent input variables
    """
    parameters = primary_idx.columns[1:]
    for col in parameters:
        ratio = primary_idx[col]/primary_idx[col].mean()

        if L_SCHALTER:
            if col == "Reisezeit Vehältnis":
                primary_idx[col] = round((2 - ratio) * 100, 2)  # for percentage
            elif col == "Umsteigezeitverhältnis":
                primary_idx[col] = round((2 - ratio) * 100, 2)
            elif col == "Umsteigezwang":
                primary_idx[col] = round((2 - ratio) * 100, 2)
            else:
                primary_idx[col] = round(ratio * 100, 2)  # for percentage
        else:
            if col == "Reisezeit Vehältnis":
                primary_idx[col] = round((2 - ratio) * 100, 2)
            else:
                primary_idx[col] = round(ratio * 100, 2)

    return primary_idx