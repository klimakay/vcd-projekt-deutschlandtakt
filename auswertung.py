"""My Module description."""

from pathlib import Path

import pandas as pd

COL_DESTINATION = 'Verbindung nach'


# ToDo I would use Path from pathlib (for reason stated in the last lecture)
def read_all_data(file_path: Path) -> dict[str, pd.DataFrame]:
    """
    Reads the input of a .xlsx file containing the evaluation of each connection. Outputs the entire .xlsx file,
    as well as the name of each sheet, which indicates the departure station.

    # ToDo great idea to mention this! Normally we do this after the return like below
    Raises TypeError if filename is not a .xlsx file.

    :param filename: name of the .xlsx evaluation file
    :return: Entire Excel sheet (data), names of all sheets (sheet_names)
    :raise: TypeError if filename is not a .xlsx file.
    """

    if file_path.suffix == ".xlsx":
        data = pd.read_excel(file_path, sheet_name=None)
        # ToDo returning the sheet_names is redundant, as they are the keys of the dict
        return data

    # ToDo else is redundant as we return and escape this function anyways
    #  return kinda behaves like brake
    #  and I like to use anti pattern, to if file_path.suffix != ".xlsx":
    #  raise ValueError
    #  And than the mean well behaved code follows
    else:
        # ToDo TypeError is used if an unsupported operation is called on a type:
        #  see https://docs.python.org/3/library/exceptions.html#TypeError
        #  I would use ValueError. This most often suited for cases that the function
        #  does not cover
        raise TypeError("The input must be a .xlsx file")

def calculation_grundlegend(schedule_data: pd.DataFrame, place: str) -> pd.DataFrame:
    """
    Calulates all basic parameters for evaluation: Reisezeit (ra),
    Beförderungsgeschwindigkeit (bg), Komfort (as) and Taktfrequenz (zv).

    :param schedule_data: The entire schedule Excel sheet.
    :param place: Indicates the departure station.
    :return: basic_params: a pd.DataFrame including all basic parameters to be calculated.
    """

    # ToDo the typing is slightly of. it is not a df but a Series
    #  (since you access a single column)
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

    # ToDo now this function takes in only the necessary data
    #  (this assignment now is obsolete left it for easier comparison)
    data = schedule_data
    cols = data.columns

    # ToDo if for some reason the order of the data alters
    #  (depending on database that might happen) it is best to access it by column name
    #  you can do this via a constant (use that mainly for autocompletion
    #  because i am lazy) otherwise strings are totally fine.
    destination = data[COL_DESTINATION]
    t_bahn = data[cols[1]]
    t_auto = data[cols[2]]
    s_bahn = data[cols[3]]
    s_auto = data[cols[4]]
    taktfrequenz = data[cols[5]]

    # ToDo could directly parse the series
    ra = reisezeit(zeit_bahn=data[cols[1]], zeit_auto=t_auto)
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
    file_name = "Auswertung Fahrplan 2025.xlsx"
    data_path = Path("data")
    evaluation = read_all_data(data_path / file_name)
    locations = evaluation.keys()

    # ToDo you could collect the results in a single df for further analytics, saving,
    #  etc.
    for location in locations:
        print(calculation_grundlegend(evaluation[location], location))
