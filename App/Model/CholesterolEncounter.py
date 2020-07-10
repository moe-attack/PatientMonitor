from .Encounter import Encounter


class CholesterolEncounter(Encounter):


    def __init__(self, date_time, cholesterol):
        """
        Constructor for Encounter subclass for cholesterol measurement
        :param date_time: Date and time of Encounter in string format
        :param cholesterol: Cholesterol value in mg/dL
        """
        Encounter.__init__(self, date_time)
        self.__cholesterol = cholesterol

    def getValue(self):
        """
        Get cholesterol value
        :return: cholesterol value
        """
        return self.__cholesterol
