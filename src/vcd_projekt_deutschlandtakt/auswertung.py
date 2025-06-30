import pandas as pd

def read_all_data(filename: str) -> tuple[dict[str, pd.DataFrame], list[int | str]]:
    """
    Reads the input of a .xlsx file containing the evaluation of each connection. Outputs the entire .xlsx file,
    as well as the name of each sheet, which indicates the departure station.

    Raises TypeError if filename is not a .xlsx file.

    :param filename: name of the .xlsx evaluation file
    :return: Entire Excel sheet (data), names of all sheets (sheet_names)
    """

    if filename.endswith(".xlsx"):
        path = "../../data/"
        data = pd.read_excel(path + filename, sheet_name=None)
        sheet_names = pd.ExcelFile(path + filename).sheet_names
        return data, sheet_names

    else:
        raise TypeError("The input must be a .xlsx file")

def calculation_grundlegend(schedule: dict[str, pd.DataFrame], place: str) -> pd.DataFrame:
    """
    Calulates all basic parameters for evaluation: Reisezeit (ra),
    Beförderungsgeschwindigkeit (bg), Komfort (as) and Taktfrequenz (zv).

    :param schedule: The entire schedule Excel sheet.
    :param place: Indicates the departure station.
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
                                     umsteigezeit=0) -> pd.DataFrame:
        """
        Calculate the pure travel speed with the distance traveled and the pure travel time with the train.

        :param strecke_bahn: Distance traveled by train in km.
        :param zeit_bahn: Time traveled by train in min.
        :param umsteigezeit: Time for transit in minute. Note that it is 0 by default, for cases when no transits are
        necessary.
        :return:
        """

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

    def takt(taktfrequenz: pd.DataFrame) -> pd.DataFrame:
        """
        Gives back the number of trains per hour (taktfrequenz)
        :param taktfrequenz: number of trains/hour
        :return: taktfrequenz (number of trains/hour)
        """
        return round(taktfrequenz,2)

    data = schedule[place]
    cols = data.columns

    destination = data[cols[0]]
    t_bahn = data[cols[1]]
    t_auto = data[cols[2]]
    s_bahn = data[cols[3]]
    s_auto = data[cols[4]]
    taktfrequenz = data[cols[5]]

    ra = reisezeit(zeit_bahn=t_bahn,zeit_auto=t_auto)
    bg = befoerderungsgeschwindigkeit(strecke_bahn=s_bahn,zeit_bahn=t_bahn)
    ks = komfort(strecke_bahn=s_bahn, strecke_auto=s_auto)
    zv = takt(taktfrequenz)

    basic_params = pd.DataFrame({"Ziel": destination,
                                 "Reisezeit Verhältnis": ra,
                                 "Beförderungsgeschwindigkeit": bg,
                                 "Komfort": ks,
                                 "Taktfrequenz": zv})

    return basic_params

#Testcase
if __name__ == '__main__':
    """
    First Evaluation only for Jahresfahrplan 2025, to check if the code works correct
    """
    evaluation, locations = read_all_data("Auswertung Fahrplan 2025.xlsx")

    for location in locations:
        print(calculation_grundlegend(evaluation, location))
