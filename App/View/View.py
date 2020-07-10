import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class View:
    def __init__(self, root):
        # Configure the UI elements
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack()
        self.canvas = tk.Canvas(self.frame)
        self.innerFrame = tk.Frame(self.canvas)

        self.__cholesterolGraph = None
        self.__bloodGraph = None

        # Main horizontal and vertical scrollbars
        self.scrollbar = tk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)
        self.verticalScrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.scrollbar.set, yscrollcommand=self.verticalScrollbar.set)

        self.scrollbar.pack(side="bottom", fill="x")
        self.verticalScrollbar.pack(side="left", fill="y")

        # Put canvas in frame and enable scrolling 
        self.canvas.pack()
        self.canvas.create_window((0, 0), window=self.innerFrame, anchor='nw')
        self.innerFrame.bind("<Configure>", lambda event: self.canvas.configure(
            scrollregion=self.canvas.bbox("all"),
            width=1200,
            height=600))

        # Setup prac ID UI
        tk.Label(self.innerFrame, text="Enter practitioner ID").grid(column=0, row=0)
        self.pracIdInput = tk.Entry(self.innerFrame)
        self.pracIdButton = tk.Button(
            self.innerFrame,
            text="Login",
        )
        # Setup N UI
        tk.Label(self.innerFrame, text="Enter N value").grid(column=0, row=1)
        self.NInput = tk.Entry(self.innerFrame)
        self.NButton = tk.Button(
            self.innerFrame,
            text="Submit",
        )
        # Setup X UI
        tk.Label(self.innerFrame, text="Enter X value").grid(column=0, row=2)
        self.XInput = tk.Entry(self.innerFrame)
        self.XButton = tk.Button(
            self.innerFrame,
            text="Submit",
        )
        # Setup Y UI
        tk.Label(self.innerFrame, text="Enter Y value").grid(column=0, row=3)
        self.YInput = tk.Entry(self.innerFrame)
        self.YButton = tk.Button(
            self.innerFrame,
            text="Submit",
        )
        # Set Up All Patient List
        tk.Label(self.innerFrame, text='All Patients', relief="ridge").grid(column=3, row=0)
        allPatientCol = ('ID', 'Name', 'Monitor Cholesterol', 'Monitor Blood Pressure')
        self.allPatientTree = ttk.Treeview(self.innerFrame, columns=allPatientCol, show='headings')
        for col in allPatientCol:
            self.allPatientTree.heading(col, text=col)

        # set up patient scroll bar
        self.patientScrollbar = tk.Scrollbar(self.innerFrame, orient="vertical", command=self.allPatientTree.yview)
        self.allPatientTree.configure(yscrollcommand=self.patientScrollbar.set)

        # Set Monitored Cholesterol Patient
        tk.Label(self.innerFrame, text='Monitored Cholesterol Patients', relief="ridge").grid(column=5, row=0)
        cholesterolPatientCol = ('ID', 'Name', 'Cholesterol Value', 'Date', 'Extra Info')
        self.cholesterolPatientTree = ttk.Treeview(self.innerFrame, columns=cholesterolPatientCol, show='headings')
        for col in cholesterolPatientCol:
            self.cholesterolPatientTree.heading(col, text=col)

        # color scheme note
        tk.Label(self.innerFrame, text="When patient's Systolic blood pressure is above X, text is in RED", relief="ridge", foreground="#FF0000").grid(column=5, row=2)
        tk.Label(self.innerFrame, text="When patient's Diastolic blood pressure is above Y, text is in Blue", relief="ridge", foreground="#00FFFF").grid(column=5, row=3)
        tk.Label(self.innerFrame, text="When both patient's Diastolic and Systolic blood pressure is above X & Y, text is in Purple", relief="ridge", foreground="#9400D3").grid(column=5, row=4)

        # Set Monitored Blood Pressure Patient
        tk.Label(self.innerFrame, text='Monitored Blood Pressure Patients', relief="ridge").grid(column=5, row=5)
        bloodPressurePatientCol = ('ID', 'Name', 'Systolic Value', 'Diastolic Value', 'Date', 'Extra Info', 'Historic Systolic')
        self.bloodPressurePatientTree = ttk.Treeview(self.innerFrame, columns=bloodPressurePatientCol, show='headings')
        for col in bloodPressurePatientCol:
            self.bloodPressurePatientTree.heading(col, text=col)

        tk.Label(self.innerFrame, text='Monitored Historical Systolic Patients', relief="ridge").grid(column=5, row=7)
        historicalCol = ('Name', 'Historical Systolic Value')
        self.historicalTree = ttk.Treeview(self.innerFrame, columns=historicalCol, show='headings')
        for col in historicalCol:
            self.historicalTree.heading(col, text=col)
        self.historicalTree.column('#2', width=1200)

        # set up cholesterol scrollbar
        self.cholesterolScrollbar = tk.Scrollbar(self.innerFrame, orient="vertical",
                                                 command=self.cholesterolPatientTree.yview)
        self.cholesterolPatientTree.configure(yscrollcommand=self.cholesterolScrollbar.set)

        # set up blood pressure scrollbar
        self.bloodPressureScrollbar = tk.Scrollbar(self.innerFrame, orient="vertical",
                                                 command=self.bloodPressurePatientTree.yview)
        self.bloodPressurePatientTree.configure(yscrollcommand=self.bloodPressureScrollbar.set)

        # set up blood pressure scrollbar
        self.historicalScrollbar = tk.Scrollbar(self.innerFrame, orient="vertical",
                                                 command=self.historicalTree.yview)
        self.historicalTree.configure(yscrollcommand=self.historicalScrollbar.set)

        # set up tag colors
        self.cholesterolPatientTree.tag_configure("red font", foreground="#FF0000")
        self.bloodPressurePatientTree.tag_configure("red font", foreground="#FF0000")
        self.bloodPressurePatientTree.tag_configure("blue font", foreground="#00FFFF")
        self.bloodPressurePatientTree.tag_configure("purple font", foreground="#9400D3")

        self.__setUpGrid()

    def __setUpGrid(self):
        """
        This function sets up the grid for each UI elements in the view
        """
        self.pracIdInput.grid(column=1, row=0)
        self.pracIdButton.grid(column=2, row=0)
        
        self.NInput.grid(column=1, row=1)
        self.NButton.grid(column=2, row=1)
        self.XInput.grid(column=1, row=2)
        self.XButton.grid(column=2, row=2)
        self.YInput.grid(column=1, row=3)
        self.YButton.grid(column=2, row=3)
        
        self.allPatientTree.grid(column=3, row=1)
        self.patientScrollbar.grid(column=4, row=1, sticky='NS')
        
        self.cholesterolPatientTree.grid(column=5, row=1)
        self.cholesterolScrollbar.grid(column=6, row=1, sticky='NS')
        
        self.bloodPressurePatientTree.grid(column=5, row=6)
        self.bloodPressureScrollbar.grid(column=6, row=6, sticky='NS')
        
        self.historicalTree.grid(column=5, row=8)
        self.historicalScrollbar.grid(column=6, row=8, sticky = 'NS')

    def openExtraInfoWindow(self, extraInfo):
        """
        This function opens up another Tkinter window that holds extra information to display
        :param extraInfo: a string of extra information to display
        """
        window = tk.Toplevel(self.root)
        tk.Label(window, text='Extra Information', relief="ridge").grid(column=0, row=0)
        tk.Label(window, text=extraInfo, relief="ridge").grid(column=0, row=1)

    def displayCholesterolGraph(self, figure=None, update=False):
        """
        This function display the cholesterol graph
        :param figure: a Figure object that holds the image
        :param update: Bool, see if there is any update from last figure
        """
        if self.__cholesterolGraph:
            self.__cholesterolGraph.get_tk_widget().grid_forget()
        if update:
            self.__cholesterolGraph = FigureCanvasTkAgg(figure, self.innerFrame)
            self.__cholesterolGraph.get_tk_widget().grid(column=3, row=6)

    def displayBloodGraph(self, figure=None, update=False):
        """
        This function display the blood pressure graph
        :param figure: a Figure object that holds the image
        :param update: Bool, see if there is any update from last figure
        """
        if self.__bloodGraph:
            self.__bloodGraph.get_tk_widget().grid_forget()
        if update:
            self.__bloodGraph = FigureCanvasTkAgg(figure, self.innerFrame)
            self.__bloodGraph.get_tk_widget().grid(column=3, row=8)

