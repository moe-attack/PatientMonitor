from abc import ABC, abstractmethod


class Encounter(ABC):

    def __init__(self, date_time):
        self.__dateTime = date_time

    def getDateTime(self):
        """
        Get the datetime of the Encounter in string format
        :return: the datetime of the Encounter in string format
        """
        return self.__dateTime

    @abstractmethod
    def getValue(self):
        """
        Abtract method to get the measurement for an Encounter subclass, e.g. CholesterolEncounter would
        return the cholesterol value
        :return: the measurement stored
        """
        pass
