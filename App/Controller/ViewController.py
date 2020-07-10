from ..View.View import View
import tkinter as tk
import threading
import datetime

from matplotlib.figure import Figure

from ..Model.WebServiceManager import WebServiceManager
from ..Model.MonitoringList import MonitoringList
from ..Model.MonitoringListAverage import MonitoringListAverage
from ..Model.Practitioner import Practitioner


class ViewController:
    def __init__(self, root):
        self.__view = View(root)
        # Default Values for Frequency, X and Y.
        self.__freq = 20
        self.__xValue = 140
        self.__yValue = 90
        self.__practitioner = None
        self.__wsm = WebServiceManager()
        self.__patients = None
        self.__monitoringList = MonitoringListAverage(self.__wsm, "cholesterol")
        self.__systolicMonitor = MonitoringList("systolic", self.__wsm, self.__xValue, 1)
        self.__systolicMonitorHistoric = MonitoringList("systolic", self.__wsm, self.__xValue, 5)
        self.__diastolicMonitor = MonitoringList("diastolic", self.__wsm, self.__yValue, 1)
        # Configure the actions in View, by passing references, View will not know existence of controller.
        self.__view.pracIdButton.config(command=self.login)
        self.__view.NButton.config(command=self.updateN)
        self.__view.XButton.config(command=self.updateX)
        self.__view.YButton.config(command=self.updateY)
        self.__view.allPatientTree.bind('<ButtonRelease-1>', self.selectedAllPatientTree)
        self.__view.cholesterolPatientTree.bind('<ButtonRelease-1>', self.selectedCholesterolPatientTree)
        self.__view.bloodPressurePatientTree.bind('<ButtonRelease-1>', self.selectedBloodPressurePatientTree)

    def login(self):
        """
        This function gets the input from UI entry as practitioner ID, and attempt to use it to fetch all patients.
        If successful, display all patients and also start the time loop function.
        """
        pracId = self.__view.pracIdInput.get()
        self.practitionerLogin(pracId)
        self.__patients = self.getAllPatients()
        self.displayAllPatientTree()
        self.timerFunction()

    def updateN(self):
        """
        This function updates the local frequency variable from the user input
        """
        self.__freq = int(self.__view.NInput.get())
        print("New N: {0}".format(self.__freq))

    def updateX(self):
        """
        This function updates the local X variable from the user input
        """
        self.__xValue = int(self.__view.XInput.get())
        print("New X: {0}".format(self.__xValue))

    def updateY(self):
        """
        This function updates the local Y variable from the user input
        """
        self.__yValue = int(self.__view.YInput.get())
        print("New Y: {0}".format(self.__yValue))

    def timerFunction(self):
        """
        This function prints the current datetime, then proceed to update every table presenting in the UI.
        Once done, the thread gets invoked again with the updated frequency.
        """
        t = datetime.datetime.now()
        st = t.strftime('Last Updated - %H:%M:%S (H:M:S)')
        print(st)
        self.displayCholesterolPatientTree()
        self.displayBloodPressurePatientTree()
        self.displayHistoricBloodPressurePatientTree()
        self.displayCholesterolGraph()
        self.displayBloodGraph()
        threading.Timer(self.__freq, self.timerFunction).start()

    def insertAllPatientTree(self, patient):
        """
        This function inserts an Patient to allPatientTree in UI
        :param patient: a Patient
        """
        self.__view.allPatientTree.insert("", "end",
                                          values=(patient.getId(), patient.getFullName(), 'Click Here', 'Click Here'))

    def practitionerLogin(self, prac_id):
        """
        This function will use the provided id to login for a practitioner (create an instance of it).
        :param prac_id: the practitioner ID used for login
        """
        loggedIn = False
        while not loggedIn:
            try:
                self.__practitioner = Practitioner(prac_id, self.__wsm)
                loggedIn = True
            except Exception:
                print("Login failed, please try again")

    def getAllPatients(self):
        """
        This function will return a list of patient to display.
        :return: patientsToDisplay: A list of patient to display.
        """
        patientsToDisplay = self.__practitioner.returnPatients()
        return patientsToDisplay

    def displayAllPatientTree(self):
        """
        This function updates the allPatientTree in UI with the current holding patients in ViewController
        """
        for patientId in self.__patients:  # for each patient, invoke the push function
            patient = self.__patients[patientId]
            self.insertAllPatientTree(patient)

    def selectedAllPatientTree(self, event):
        """
        This function is the handler when user interacts with cells in allPatientTree
        :param event: the user event that happened
        """
        curItem = self.__view.allPatientTree.item(self.__view.allPatientTree.focus())
        col = self.__view.allPatientTree.identify_column(event.x)
        if col == '#3':
            # monitor cholesterol
            self.monitorCholesterol(str(curItem['values'][0]))
            self.displayCholesterolPatientTree()
        if col == '#4':
            # monitor BP implementation
            self.monitorBloodPressure(str(curItem['values'][0]))
            self.displayBloodPressurePatientTree()

    def selectedCholesterolPatientTree(self, event):
        """
        This function is the handler of user interactions with cells in cholesterolPatientTree
        :param event: the user event that happened
        """
        curItem = self.__view.cholesterolPatientTree.item(self.__view.cholesterolPatientTree.focus())
        col = self.__view.cholesterolPatientTree.identify_column(event.x)
        if col == '#5':
            patient = self.__monitoringList.returnPatients()[str(curItem['values'][0])]
            self.__view.openExtraInfoWindow(patient.getExtraInfo())

    def selectedBloodPressurePatientTree(self, event):
        """
         This function is the handler of user interactions with cells in bloodPressurePatientTree
        :param event: the user event that happened
        """
        curItem = self.__view.bloodPressurePatientTree.item(self.__view.bloodPressurePatientTree.focus())
        col = self.__view.bloodPressurePatientTree.identify_column(event.x)
        if col == '#6':
            patient = self.__systolicMonitor.returnPatients()[str(curItem['values'][0])]
            self.__view.openExtraInfoWindow(patient.getExtraInfo())
        if col == '#7':
            self.monitorHistoricBloodPressure(str(curItem['values'][0]))
            self.displayHistoricBloodPressurePatientTree()

    def monitorCholesterol(self, patient_id):
        """
        This function will update the local data using the provided patient id.
        :param patient_id: the provided Patient id.
        """
        if self.__monitoringList.contains(patient_id):  # click means remove
            self.__monitoringList.remove(patient_id)
        else:  # click means add
            monitoredPatient = self.__practitioner.getPatient(patient_id)
            if monitoredPatient:
                cholesterolEncounters = self.__wsm.fetchEncounter(patient_id, "cholesterol", 1)
                if cholesterolEncounters:
                    monitoredPatient.updateEncounters(cholesterolEncounters)
                else:
                    monitoredPatient.updateEncounters(None)
                self.__monitoringList.add(monitoredPatient)

    def displayCholesterolPatientTree(self):
        """
        This function updates the cholesterolPatientTree in UI with the current holding patients in ViewController
        """
        self.__view.cholesterolPatientTree.delete(*self.__view.cholesterolPatientTree.get_children())
        patientsMonitored = self.__monitoringList.returnPatients()
        for patientId in patientsMonitored:  # for each patient, invoke the pushMonior function
            patient = patientsMonitored[patientId]
            self.insertCholesterolPatientTree(patient)

    def insertCholesterolPatientTree(self, patient):
        """
        This function inserts a patient in the cholesterolPatientTree
        :param patient: a Patient
        """
        encounters = patient.getEncounters()
        if encounters:
            encounter = encounters[0]
            value = encounter.getValue()
            if value > round(self.__monitoringList.getAverage(), 2):
                # display in red
                self.__view.cholesterolPatientTree.insert("", "end", values=(
                    patient.getId(), patient.getFullName(), str(value), encounter.getDateTime(), 'Click Here'),
                                                          tags=("red font",))
            else:
                # display in plain background
                self.__view.cholesterolPatientTree.insert("", "end", values=(
                    patient.getId(), patient.getFullName(), str(value), encounter.getDateTime(), 'Click Here'))
        else:
            # no encounter
            self.__view.cholesterolPatientTree.insert("", "end", values=(
                patient.getId(), patient.getFullName(), 'No Data', 'N/A', 'Click Here'))

    def displayCholesterolGraph(self):
        """
        This function display the cholesterol graph in UI
        """
        if self.__monitoringList.getNumPatients() > 0:
            patients = self.__monitoringList.returnPatients()
            names = []
            values = []
            for patient_id in patients:
                encounters = patients[patient_id].getEncounters()
                if encounters:
                    names.append(patients[patient_id].getFullName())
                    values.append(patients[patient_id].getEncounters()[0].getValue())
            f = Figure(figsize=(8, 2))
            a = f.add_subplot(111)
            a.bar(names, values)
            a.set_title("Total Cholesterol mg/dL")
            self.__view.displayCholesterolGraph(f, True)
        else:
            self.__view.displayCholesterolGraph()

    def monitorBloodPressure(self, patient_id):
        """
        This function updates the local data with newly selected patient_id
        :param patient_id: the ID of a patient
        :return:
        """
        # check if the id already exists in local data, if yes, remove it.
        if self.__systolicMonitor.contains(patient_id):  # click means remove
            self.__systolicMonitor.remove(patient_id)
            self.__diastolicMonitor.remove(patient_id)
            if self.__systolicMonitorHistoric.contains(patient_id):  # Should also remove from long term monitor
                self.__systolicMonitorHistoric.remove(patient_id)
        else:  # click means add
            monitoredPatientSystolic = self.__practitioner.getPatient(patient_id)
            if monitoredPatientSystolic:
                monitoredPatientDiastolic = self.__practitioner.getPatient(patient_id)
                systolicEncounters = self.__wsm.fetchEncounter(patient_id, "systolic", 1)
                diastolicEncounters = self.__wsm.fetchEncounter(patient_id, "diastolic", 1)
                if systolicEncounters:
                    monitoredPatientSystolic.updateEncounters(systolicEncounters)
                    monitoredPatientDiastolic.updateEncounters(diastolicEncounters)
                self.__systolicMonitor.add(monitoredPatientSystolic)
                self.__diastolicMonitor.add(monitoredPatientDiastolic)

    def displayBloodPressurePatientTree(self):
        """
        This function updates the bloodPressurePatientTree in UI with the current holding patients in ViewController
        """
        self.__view.bloodPressurePatientTree.delete(*self.__view.bloodPressurePatientTree.get_children())
        patientsSystolic = self.__systolicMonitor.returnPatients()
        patientsDiastolic = self.__diastolicMonitor.returnPatients()
        for patient_id in patientsSystolic:
            self.insertBloodPressurePatientTree(patientsSystolic[patient_id], patientsDiastolic[patient_id])

    def insertBloodPressurePatientTree(self, patientSystolic, patientDiastolic):
        """
        This function inserts a patient into systolic and diastolic BP graph
        :param patientSystolic: patient with systolic encounter
        :param patientDiastolic: same patient with diastolic encounter
        :return:
        """
        diastolicEncounters = patientDiastolic.getEncounters()
        systolicEncounters = patientSystolic.getEncounters()
        displayValueSystolic = "No Data"
        displayValueDiastolic = "No Data"
        date = "No data"
        highlight = None

        id = patientSystolic.getId()
        name = patientSystolic.getFullName()

        if systolicEncounters:
            date = systolicEncounters[0].getDateTime()
            displayValueSystolic = systolicEncounters[0].getValue()
            if self.__xValue:
                if displayValueSystolic > round(self.__xValue, 2):
                    highlight = 'systolic'

        if diastolicEncounters:
            date = diastolicEncounters[0].getDateTime()
            displayValueDiastolic = diastolicEncounters[0].getValue()
            if self.__yValue:
                if displayValueDiastolic > round(self.__yValue, 2):
                    if highlight == 'systolic':
                        highlight = 'allBloodPressure'
                    else:
                        highlight = 'diastolic'

        if highlight == 'systolic':
            self.__view.bloodPressurePatientTree.insert("", "end", values=(
                id, name, str(displayValueSystolic), str(displayValueDiastolic), date, 'Click Here', 'Click Here'),
                                                        tags=("red font",))
        elif highlight == 'diastolic':
            self.__view.bloodPressurePatientTree.insert("", "end", values=(
                id, name, str(displayValueSystolic), str(displayValueDiastolic), date, 'Click Here', 'Not Available'),
                                                        tags=("blue font",))
        elif highlight == 'allBloodPressure':
            self.__view.bloodPressurePatientTree.insert("", "end", values=(
                id, name, str(displayValueSystolic), str(displayValueDiastolic), date, 'Click Here', 'Click Here'),
                                                        tags=("purple font",))
        else:
            self.__view.bloodPressurePatientTree.insert("", "end", values=(
                id, name, str(displayValueSystolic), str(displayValueDiastolic), date, 'Click Here', 'Not Available'))

    def monitorHistoricBloodPressure(self, patient_id):
        """
        This function adds a patient into historic BP monitor
        :param patient_id: the ID of a patient to be added
        """
        if self.__systolicMonitorHistoric.contains(patient_id):  # click means remove
            self.__systolicMonitorHistoric.remove(patient_id)
        else:
            latestEncounter = self.__systolicMonitor.getNthEncounter(patient_id, 0)
            if latestEncounter and latestEncounter.getValue() > self.__xValue:  # Only monitor if systolic is higher than X
                monitoredPatient = self.__practitioner.getPatient(patient_id)
                if monitoredPatient:
                    # fetch systolic encounter with past 5 values
                    systolicEncounters = self.__wsm.fetchEncounter(patient_id, "systolic", 5)
                    if systolicEncounters:
                        monitoredPatient.updateEncounters(systolicEncounters)
                    self.__systolicMonitorHistoric.add(monitoredPatient)

    def displayHistoricBloodPressurePatientTree(self):
        """
        This function updates the historicBloodPressureTree in UI by using local data
        """
        self.__view.historicalTree.delete(*self.__view.historicalTree.get_children())
        patients = self.__systolicMonitorHistoric.returnPatients()
        for patient_id in patients:
            patient = patients[patient_id]
            self.insertHistoricBloodPressurePatientTree(patient)

    def insertHistoricBloodPressurePatientTree(self, patient):
        """
        This function inserts a patient into the historicalTree in UI
        :param patient: a Patient
        """
        encounters = patient.getEncounters()
        productString = ""
        for encounter in encounters:
            productString += "{0} ({1}),".format(encounter.getValue(), encounter.getDateTime())
        productString = productString[:-1]
        self.__view.historicalTree.insert("", "end", values=(patient.getFullName(), productString))

    def displayBloodGraph(self):
        """
        This function display the blood monitoring graph in UI
        :return:
        """
        if self.__systolicMonitorHistoric.getNumPatients() > 0:
            patients = self.__systolicMonitorHistoric.returnPatients()
            names = []
            indices = [1, 2, 3, 4, 5]
            f = Figure(figsize=(8, 2))
            a = f.add_subplot(111)
            a.set_xticks(indices)
            for patient_id in patients:
                encounters = patients[patient_id].getEncounters()
                if encounters:
                    names.append(patients[patient_id].getFullName())
                    values = [encounter.getValue() for encounter in encounters]
                    a.plot(indices[:len(values)], values)
            a.legend(names, loc='best')
            a.set_title("Systolic BP (mmHg)")
            self.__view.displayBloodGraph(f, True)
        else:
            self.__view.displayBloodGraph()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("FIT3077 Assignment 3")
    vc = ViewController(root)
    root.mainloop()
