import copy


class Patient:

    def __init__(self, id, fname, lname, birthdate, gender, street, city, state, country):
        self.__id = id
        self.__fname = fname
        self.__lname = lname
        self.__birthdate = birthdate
        self.__gender = gender
        self.__street = street
        self.__city = city
        self.__state = state
        self.__country = country
        self.__encounters = [] # Encounter instance of measurement to be monitored

    def updateEncounters(self, encounters):
        """
        Replace or set current encounters with another (new) list of Encounters
        :param encounters: List of Encounters
        :return: None
        """
        self.__encounters = encounters

    def getFullName(self):
        """
        Get the full name of the patient
        :return: String of patient's first and last names
        """
        return "{0} {1}".format(self.__fname, self.__lname)

    def getExtraInfo(self):
        """
        Get the extra information needed when selecting a monitored patient
        :return: String with birthdate, gender and address of patient
        """
        bdayString = "Birthdate: {0}".format(self.__birthdate)
        genderString = "Gender: {0}".format(self.__gender)
        addressString = "Address: {0}, {1}, {2}, {3}".format(self.__street, self.__city, self.__state, self.__country)
        return "{0}\t\t{1}\t\t{2}".format(bdayString, genderString, addressString)

    def getId(self):
        """
        Get the ID of the patient
        :return: The ID of the patient
        """
        return self.__id

    def getEncounters(self):
        """
        Get the Encounters list in the patient
        :return: Deep copy of the Encounter list to prevent security leaks
        """
        if self.__encounters:
            return copy.deepcopy(self.__encounters)
        return
