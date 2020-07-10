import copy
from .WebServiceManager import WebServiceManager


class MonitoringList():

    def __init__(self, encounterType, wsm, threshold=-1, num=1):
        self.__patients = dict()  # Patient ID to Patient instances
        self.__encounterType = encounterType  # String denoting type of measurement being monitored
        self.__threshold = threshold
        self.__wsm = wsm
        self.__numHistoric = num

    def add(self, patient):
        """
        Add a Patient to be monitored and get their Encounter
        :param patient: The Patient to be added
        :return: True if patient was added, false otherwise
        :postcondition: Patient is now being monitored and average has been updated if measurement was found
        """
        patient_id = patient.getId()
        if patient_id not in self.__patients:
            self.__patients[patient_id] = patient
            return True
        return False

    def remove(self, patient_id):
        """
        Unmonitor a patient
        :param patient_id: ID of patient to be unmonitored
        :return: None
        :precondition: patient_id must correspond to a patient in self.__patients
        """
        if patient_id in self.__patients:
            del self.__patients[patient_id]

    def contains(self, patient_id):
        """
        Checks if patient is being monitored
        :param patient_id: ID of patient to check
        :return: True if patient_id is a valid key, False otherwise
        """
        return patient_id in self.__patients

    def returnPatients(self):
        """
        Get the patients being monitored
        :return: Deep copy of the patients dictionary to prevent security leaks
        """
        return copy.deepcopy(self.__patients)

    def update(self):
        """
        Called every N seconds to look for new measurements only for patients who had no measurements upon login
        (as we were instructed). Updates the data based on these new measurements.
        :return: None
        :postcondition: Patient measurements are all updated (excluding those who had no measurements upon login)
        """
        patient_ids = list(self.__patients.keys())  # to avoid change of iterable size while updating
        for patient_id in patient_ids:
            if patient_id in self.__patients:
                encounters = self.__patients[patient_id].getEncounters()
                if encounters: # Only look for new encounter if encounter already exists
                    latest_curr_encounter = encounters[0]
                    new_encounters = self.__wsm.fetchEncounter(patient_id, self.__encounterType, self.__numHistoric)
                    if new_encounters and new_encounters[0].getDateTime() != latest_curr_encounter.getDateTime(): # only update if recent encounter is different
                        self.__patients[patient_id].updateEncounters(new_encounters)

    def getPatientIds(self):
        """
        Get list of IDs of all the Patients being monitored (including those with no measurement)
        :return: list of patient ids
        """
        return(list(self.__patients.keys()))


    def getNthEncounter(self, patient_id, n):
        """
        Gets the nth Encounter of a Patient
        :param patient_id: ID of Patient who's Encounter we are getting
        :param n: The Encounter number (starting from 0) to get. n=0 refers to the latest encounter
        :return: The nth Encounter
        """
        if self.contains(patient_id):
            encounters = self.__patients[patient_id].getEncounters()
            if encounters and len(encounters) > n:
                return encounters[n]

    def getThreshold(self):
        """
        Get threshold value (e.g. for highlighting high values)
        :return: tTreshold value
        """
        return self.__threshold

    def setThreshold(self, newThreshold):
        """
        Set new threshold value
        :param newThreshold: New threshold value
        :return: None
        """
        self.__threshold = newThreshold

    def getNumPatients(self):
        """
        Get the number of patients being monitored
        :return: Number of patients being monitored (including those with no measurement)
        """
        return len(self.__patients)


