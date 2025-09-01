"""
    All functions are stored here that are used to read data, evaluate the general parameters (step 1), and the
    reachability index (step 2).
"""


from pathlib import Path

import pandas as pd
from pandas import DataFrame, Series

COL_DESTINATION = 'Verbindung nach'


def read_all_data(file_path: Path) -> dict[str, DataFrame] | None:
    """
    Reads the input of a .xlsx file containing the evaluation of each connection. Outputs the entire .xlsx file,
    as well as the name of each sheet, which indicates the departure station.


    :param file_path: path and name of the .xlsx evaluation file
    :return: Entire Excel sheet (data) in file_path
    :raise: ValueError if file_path is not a .xlsx file.
    """

    if file_path.suffix == ".xlsx":
        # ToDo you could read this with an context manager (with statement)
        #  to ensure resources are freed if the file does not exists
        data = pd.read_excel(file_path, sheet_name=None)
        return data

    raise ValueError("The input must be a .xlsx file")

    # ToDo this None return will never be reached - so it is redundant.
    return None


def calculation_grundlegend(schedule_data: pd.DataFrame, schalter = False) -> pd.DataFrame:
    """
    Calulates all basic parameters for evaluation: Reisezeit (ra),
    Beförderungsgeschwindigkeit (bg), Komfort (as) and Taktfrequenz (zv).

    # ToDo schalter could use a more descriptive name (consider_transits)
    :param schalter: Determines if transits are considered or not.
    :param schedule_data: The entire schedule Excel sheet.
    :return: basic_params: a pd.DataFrame including all basic parameters to be calculated.
    """

    # ToDo the functions exists only in the scope of this function.
    #  However, they seem quite standalone, so you could put them in outer scope to use
    #  elsewhere
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
        if not schalter:
            umsteigezeit = 0

        return round(strecke_bahn / (zeit_bahn - umsteigezeit), 2)


    def komfort(strecke_bahn: pd.DataFrame, strecke_auto: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates the comfort index by dividing the distance traveled by train in km with the distance traveled
        by car in km.

        :param strecke_bahn: Distance traveled by train in km.
        :param strecke_auto: Distance traveled by car in km.
        :return: Komfort (%)
        """

        return round(strecke_bahn / strecke_auto, 2)


    def takt(frequenz: pd.DataFrame) -> pd.DataFrame:
        """
        Gives back the number of trains per hour (taktfrequenz)
        :param frequenz: number of trains/hour
        :return: taktfrequenz (number of trains/hour)
        """
        return round(frequenz,2)


    data = schedule_data
    cols = data.columns
    # ToDo I like the constant (I think it might was a comment from last it?)
    #  but I would use it for all column to be constant
    destination = data[COL_DESTINATION]
    t_bahn = data[cols[1]]
    t_auto = data[cols[2]]
    s_bahn = data[cols[3]]
    s_auto = data[cols[4]]
    taktfrequenz = data[cols[5]]

    # ToDO the functions you be defined anyway. There is no overhead, as both cases are
    #  loaded/check anyway before runtime and are only executed on runtime
    if schalter:

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

        t_u = data[cols[6]]
        u = data[cols[7]]
        ra = reisezeit(zeit_bahn=t_bahn, zeit_auto=t_auto)
        bg = befoerderungsgeschwindigkeit(strecke_bahn=s_bahn, zeit_bahn=t_bahn, umsteigezeit=t_u)
        ks = komfort(strecke_bahn=s_bahn, strecke_auto=s_auto)
        zv = takt(taktfrequenz)
        ua = umsteigezeit_ratio(zeit_bahn=t_bahn, umsteigezeit=t_u)
        uv = umsteigezwang(strecke_bahn=s_bahn, anzahl_umsteigevorgang=u)

        # ToDo you  have some code duplication below. Why dont create the dict with the
        #  base case and update it is the condition is given?
        basic_params = pd.DataFrame({"Ziel": destination,
                                     "Reisezeit Verhältnis": ra,
                                     "Beförderungsgeschwindigkeit": bg,
                                     "Komfort": ks,
                                     "Taktfrequenz": zv,
                                     "Umsteigezeitverhältnis": ua,
                                     "Umsteigezwang": uv})

    else:
        ra = reisezeit(zeit_bahn=t_bahn, zeit_auto=t_auto)
        bg = befoerderungsgeschwindigkeit(strecke_bahn=s_bahn, zeit_bahn=t_bahn)
        ks = komfort(strecke_bahn=s_bahn, strecke_auto=s_auto)
        zv = takt(taktfrequenz)
        basic_params = pd.DataFrame({"Ziel": destination,
                                     "Reisezeit Verhältnis": ra,
                                     "Beförderungsgeschwindigkeit": bg,
                                     "Komfort": ks,
                                     "Taktfrequenz": zv})

    return basic_params


def gewichtung(primary_idx: pd.DataFrame, schalter = False) -> Series | DataFrame:
    """
    Calculates a weighted index for time-dependent and distance-independent input variables.
    :param schalter: A bool that dDetermines if transits are considered or not.
    :param primary_idx: Dataframe that consists of the primary parameters for different origins to a certain
    destination.
    :return primary_idx: A new pd.Series or pd.DataFame based on the input DataFrame that consists of the weighted
    index for time-dependent and distance-independent input variables.
    """
    # ToDo analog comments to function above
    primary_idx.set_index("Ziel", drop=True, inplace=True)
    parameters = primary_idx.columns[:]
    for col in parameters:
        ratio = primary_idx[col]/primary_idx[col].mean()

        if schalter:
            # Gewichtungsfaktoren
            d = {"Komfort": 0.242,
                 "Reisezeit Verhältnis": 0.379,
                 "Beförderungsgeschwindigkeit": 0.131,
                 "Taktfrequenz": 0.072,
                 "Umsteigezeitverhältnis": 0.088,
                 "Umsteigezwang": 0.088
                 }

            if col == "Reisezeit Vehältnis":
                primary_idx[col] = (2 - ratio) * 100  # for percentage
            elif col == "Umsteigezeitverhältnis":
                primary_idx[col] = (2 - ratio) * 100
            elif col == "Umsteigezwang":
                primary_idx[col] = (2 - ratio) * 100
            else:
                primary_idx[col] = ratio * 100  # for percentage

            primary_idx[col] = primary_idx[col] * d[col]

        else:
            # Gewichtungsfaktoren
            d = {"Komfort": 0.294,
                 "Reisezeit Verhältnis": 0.460,
                 "Beförderungsgeschwindigkeit": 0.159,
                 "Taktfrequenz": 0.087,
                 }

            if col == "Reisezeit Vehältnis":
                primary_idx[col] = (2 - ratio) * 100
            else:
                primary_idx[col] = ratio * 100

            primary_idx[col] = primary_idx[col] * d[col]

    return primary_idx

def erschliessungsqualitaet(weighted_idx: DataFrame) -> dict:
    """
    Calculates the sum of the different weighted parameters per line, so over all destinations

    :param weighted_idx: Contains the different weighted indexes from function gewichtung.
    :return eq: a dictionary which contains the sums of weighted index.
    """
    destinations = weighted_idx.index.values
    eq = {}
    for dest in destinations:
        # ToDO what is this comment about?
        eq[dest] = weighted_idx.loc[dest].sum()  # weighted_idx.loc[dest].sum() is the e
    return eq

# ToDo what about formatting as the function name?
def resultat(eq_wert: dict) -> float:
    """
    This function converts in the end first the input dictionary to a Dataframe and then the mean over
    the whole number of destinations. This is the final result.
    :param eq_wert: input dictionary which contains the sums of weighted index over all destinations.
    :return eq_ort: the mean over all destinations.
    """
    eq_df = pd.DataFrame.from_dict(eq_wert, orient='index')
    eq_ort = round(eq_df.values.mean(),2)
    return eq_ort
