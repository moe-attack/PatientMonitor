from .Encounter import Encounter


class SystolicEncounter(Encounter):


    def __init__(self, date_time, systolic):
        """
        Constructor for Encounter subclass for cholesterol measurement
        :param date_time: Date and time of Encounter in string format
        :param systolic: Systolic BP value in mg/dL
        """
        Encounter.__init__(self, date_time)
        self.__systolic = systolic

    def getValue(self):
        """
        Get Systolic BP value
        :return: Systolic BP value in mg/dL
        """
        return self.__systolic
