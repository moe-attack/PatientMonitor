from .Encounter import Encounter


class DiastolicEncounter(Encounter):


    def __init__(self, date_time, diastolic):
        """
        Constructor for Encounter subclass for cholesterol measurement
        :param date_time: Date and time of Encounter in string format
        :param cholesterol: Cholesterol value in mg/dL
        """
        Encounter.__init__(self, date_time)
        self.__diastolic = diastolic

    def getValue(self):
        """
        Get Diastolic BP value
        :return: Diastolic BP value in mg/dL
        """
        return self.__diastolic
