from .WebServiceManager import WebServiceManager
from .MyExceptions import LoginException
import copy


class Practitioner:

    def __init__(self, pracId, wsm):
        self.__wsm = wsm  # WebServiceManager instance for making calls to server
        self.__identifier = self.__wsm.fetchPractitionerIdentifier(pracId)  # use the ID to get the identifier using wsm
        if not self.__identifier:
            raise LoginException
        self.__patients = self.__wsm.fetchAllPatients(self.__identifier)  # use wsm to get all patients in a dictionary

    def returnPatients(self):
        """
        Get all the patients of the practitioner
        :return: Deep copy of the dictionary containing all the patients of the practitioner
        """
        return copy.deepcopy(self.__patients)

    def getPatient(self, patient_id):
        """
        Get a particular patient of the practitioner
        :param patient_id: ID of patient to get
        :return: Deep copy of Patient with ID of patient_id
        :precondition: patient_id must match the iD of a patient of the practitioner
        """

        if patient_id in self.__patients:
            return copy.deepcopy(self.__patients[patient_id])
