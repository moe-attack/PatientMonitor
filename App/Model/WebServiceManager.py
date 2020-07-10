import requests
from .CholesterolEncounter import CholesterolEncounter
from .SystolicEncounter import SystolicEncounter
from .DiastolicEncounter import DiastolicEncounter
from .Patient import Patient


class WebServiceManager:
    def __init__(self):
        # Set up all the base URL components when class initialize
        self.__baseUrl = "https://fhir.monash.edu/hapi-fhir-jpaserver/fhir/"
        self.__practitionerUrl = "Practitioner/"
        self.__patientUrl = "Patient/"
        self.__allEntriesUrl = "Encounter?participant.identifier={0}|{1}&_include=Encounter.participant.individual"
        # code 2093-3 is cholesterol value; sort by descending date; count = 1 returns only 1 result
        self.__encounterUrl = "Observation?patient={0}&code={1}&_sort=-date&_count={2}"
        self.__codes = {
            "cholesterol": "2093-3",
            "systolic": "55284-4",
            "diastolic": "55284-4"
        }

    def fetchPractitionerIdentifier(self, id):
        """
        This function builds an url to access all encounters of a certain practitioner
        :param id: Practitioner's ID
        :return: the url to access all encounters
        """
        data = requests.get(url=(self.__baseUrl + self.__practitionerUrl + id)).json()
        if data["resourceType"] == "Practitioner":
            identifier = data["identifier"][0]
            identifier_url = self.__baseUrl + self.__allEntriesUrl.format(identifier["system"], identifier["value"])
            return identifier_url
        return None

    def fetchAllPatients(self, url):
        """
        This function will get a map of Patient object
        :param url:
        :return: map of id to patient
        """
        # practitioner_name = data["entry"][0]["resource"]["participant"][0]["individual"]["display"]
        # print("Practitioner: " + practitioner_name)
        existing_patients = {}
        next_page = True
        page_count = 0
        next_url = url

        while next_page:
            data = requests.get(url=next_url).json()
            next_page = False
            if 'link' in data:
                links = data['link']
                for link in links:
                    if link['relation'] == 'next':
                        next_page = True
                        next_url = link['url']
                        page_count += 1

                if "entry" in data:
                    encounters = data["entry"]
                    for encounter in encounters:
                        patient = encounter["resource"]["subject"]
                        patient_id = patient["reference"].split('/')[1]
                        if patient_id not in existing_patients:  # check if this id has been stored
                            existing_patients[patient_id] = self.fetchPatient(patient_id)
            else:
                next_page = False  # error in FHIR server
        return existing_patients

    def fetchPatient(self, id):
        """
        This function gets a specific patient's detail base on the provided ID, and create a Patient object with it
        :param id: patient's ID
        :return: a Patient object
        """
        data = requests.get(url=(self.__baseUrl + self.__patientUrl + id)).json()
        birthdate = data["birthDate"]
        gender = data["gender"]

        address = data["address"][0]
        street = address["line"][0]
        city = address["city"]
        state = address["state"]
        country = address["country"]

        name = data["name"][0]
        fname = ''.join(char for char in name["given"][0] if char.isalpha())
        lname = ''.join(char for char in name["family"] if char.isalpha())

        patient = Patient(id, fname, lname, birthdate, gender, street, city, state, country)
        return patient

    def fetchEncounter(self, id, encounterType, num):
        """
        This function takes a patient ID and will return his/her latest cholesterol values
        :param id: the ID of a patient
        :param encounterType: Type of encounter to fetch
        :param num: Number of historic encounters to fetch
        :return: List of Encounter subclass defined by encounterType
        """
        if encounterType in self.__codes:
            code = self.__codes[encounterType]
            # Code represents cholesterol observation. Sort in decreasing order to get the last cholesterol value
            encounterUrl = self.__baseUrl + self.__encounterUrl.format(id, code, num)
            data = requests.get(encounterUrl).json()

            # If patient has observation
            if "entry" in data:
                entries = data["entry"]
                if len(entries) > 0:
                    encounters = []
                    for entry in entries:
                        item = entry['resource']
                        date = item['issued']
                        if encounterType == "cholesterol":
                            cholesterol = item['valueQuantity']['value']
                            encounters.append(CholesterolEncounter(date, cholesterol))
                        elif encounterType == "systolic":
                            components = item['component']
                            for component in components:
                                if component['code']['coding'][0]['code'] == '8480-6':  # Systolic Blood Pressure code
                                    sbp = component['valueQuantity']['value']
                            encounters.append(SystolicEncounter(date, sbp))
                        elif encounterType == "diastolic":
                            components = item['component']
                            for component in components:
                                if component['code']['coding'][0]['code'] == '8462-4':  # Diastolic Blood Pressure code
                                    dbp = component['valueQuantity']['value']
                            encounters.append(DiastolicEncounter(date, dbp))
                        else:
                            return []
                            
                    return encounters

        return []


if __name__ == "__main__":
    webServiceManager = WebServiceManager()
    identifier_url = webServiceManager.fetchPractitionerIdentifier("3337")
    patients = webServiceManager.fetchAllPatients(identifier_url)
    patient_id_mock = '3335'
    print("patient id is: {0}".format(patient_id_mock))
    patient_mock = webServiceManager.fetchPatient(patients[patient_id_mock].getId())
    # cholesterol test
    patient_mock.updateEncounter('cholesterol', webServiceManager.fetchEncounter(patient_mock.getId(), 'cholesterol'))
    print("Cholesterol Test: {0}, {1}, {2}".format(patient_mock.getId(), patient_mock.getFullName(),
                                                   patient_mock.getEncounter('cholesterol').getValue()["cholesterol"]))

    # blood pressure test
    patient_mock.updateEncounter('bloodPressure',
                                 webServiceManager.fetchEncounter(patient_mock.getId(), 'bloodPressure'))
    print("Cholesterol Test: {0}, {1}, diastolicBloodPressure: {2}, systolicBloodPressure: {3}".format(
        patient_mock.getId(), patient_mock.getFullName(),
        patient_mock.getEncounter('bloodPressure').getValue()["diastolicBloodPressure"],
        patient_mock.getEncounter('bloodPressure').getValue()['systolicBloodPressure']))
