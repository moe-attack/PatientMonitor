import copy
from .MonitoringList import MonitoringList


class MonitoringListAverage(MonitoringList):

    def __init__(self, encounterType, wsm):
        MonitoringList.__init__(self, encounterType, wsm, -1, 1)
        self.__numPatients = 0
        self.__average = -1
        

    def add(self, patient):
        """
        Add a Patient to be monitored, get their Encounter, and update the average
        :param patient: The Patient to be added
        :return: None
        :postcondition: Patient is now being monitored and average has been updated if measurement was found
        """
        wasAdded = super().add(patient)
        if wasAdded:
            encounters = patient.getEncounters()
            if encounters:
                encounter = encounters[0]
                self.__numPatients += 1
                new_value = encounter.getValue()
                if self.__numPatients == 1:
                    self.__average = new_value
                else:
                    self.__average = (self.__average * (self.__numPatients - 1) + new_value) / self.__numPatients
                super().setThreshold(self.__average)

    def remove(self, patient_id):
        """
        Unmonitor a patient and update the average
        :param patient_id: ID of patient to be unmonitored
        :return: None
        :precondition: patient_id must correspond to a patient in self.__patients
        """
        encounter = super().getNthEncounter(patient_id, 0)
        if encounter:
            self.__numPatients -= 1
            old_value = encounter.getValue()
            if self.__numPatients == 0:
                self.__average = -1
            else:
                self.__average = (self.__average * (self.__numPatients + 1) - old_value) / self.__numPatients
            super().setThreshold(self.__average)
        super().remove(patient_id)



    def __updateAverage(self):
        """
        Update the average of all exisitng patients who are being monitored. Those with no measurement are
        no counted
        :return: None
        """
        new_sum = 0
        new_total = 0
        patient_ids = super().getPatientIds()  # to avoid change of iterable size while updating
        for patient_id in patient_ids:
            encounter = super().getNthEncounter(patient_id, 0)
            if encounter:
                new_sum += encounter.getValue()
                new_total += 1
                    
        self.__numPatients = new_total
        if new_total == 0:
            self.__average = -1
        else:
            self.__average = new_sum / new_total
        super().setThreshold(self.__average)
        

    def update(self):
        """
        Update new values from server and also update the average
        :return: None
        """
        super().update()
        self.__updateAverage()
        

    def getAverage(self):
        """
        Get the average measurement value
        :return: The average measurement value
        """
        return self.__average
