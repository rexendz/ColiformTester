from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from arduino import SerialListener
import os
import sys


class Window(QWidget): # Inherits from QWidget class
    def __init__(self):
        super().__init__() # Initializes the QWidget class
        self.title = "Automated Total Coliform Test" # Title Name
        self.left = 0 # Window Coordinates
        self.top = 0  # Window Coordinates
        self.width = 480 # Window Width
        self.height = 320 # Window Height
        self.userpath = os.getenv("HOME") # Get user path directory
        self.icon = QIcon(self.userpath + '/PycharmProjects/Germz/favicon.jpg') # Get Icon Path
        self.vbox = QVBoxLayout() # Vertical Layout
        self.gbox = QGridLayout() # Gridbox Layout

    def InitWindow(self):
        self.setWindowTitle(self.title) # Sets the window title to the title name declared earlier
        self.setGeometry(self.left, self.top, self.width, self.height) # Set the dimension of the Window
        self.setStyleSheet("background-color: #424242") # Set the background color of the window to gray
        self.setWindowIcon(self.icon) # Set the window icon to the icon path declared earlier
        self.setMaximumHeight(self.height) # Constrain Dimensions
        self.setMaximumWidth(self.width)   # ^
        self.setMinimumHeight(self.height) # ^
        self.setMinimumWidth(self.width)   # ^

    def InitLayout(self):
        self.setLayout(self.vbox) # Set window layout to vertical
        self.vbox.setGeometry(QRect(self.left, self.top, self.width, self.height)) # Set geometry of layout
        self.vbox.setSpacing(10) # Set spacing of layout


class Worker1(QObject): # Worker class inherits from QObject, acts like asynctask (run from background)
    finished = pyqtSignal()  # give worker class a finished signal
    probeDetected = pyqtSignal() # give worker class a signal that emits when probe is detected (intent)

    def __init__(self, arduino, parent=None): # constructor of worker class
        QObject.__init__(self, parent=parent) # Initialize Qobject constructor
        self.arduino = arduino # Save arduino listener
        self.continue_run = True # Sets worker class to run loop or not

    def do_work(self):
        # while self.continue_run:  # give the loop a stoppable condition
            # self.arduino.resume() # Resumes python listening of arduino
            # reading = self.arduino.read() # Reads data from arduino
            # if reading == "OK": # If arduino sends data "OK"
            #    self.probeDetected.emit() # Sends signal that probe is detected
            #    self.stop() # Stops the worker
        # self.reader.pause() # Pauses reading of data from arduino
        self.finished.emit() # Sends signal that the worker has finished its task.

    def stop(self):
        self.continue_run = False # Function that Stops the loop


class StartPage(Window): # First window of the program inherits from class Window created earlier
    switch_next = pyqtSignal(QWidget) # Signal to switch to next window
    stop_signal = pyqtSignal() # Signal to stop the program

    def __init__(self, arduino): # Constructor of first page
        super().__init__() # Initializes the constructor of class Window
        self.arduino = arduino # Set arduino listener
        self.thread = None # Thread object
        self.worker = None # Worker object
        self.InitWindow() # Initialize the window
        self.InitLayout() # Initialize the layout
        self.InitComponents() # Initialize the components
        self.InitWorker() # Initialize the worker
        self.show() # Show the window

    def InitComponents(self): # This function creates the components
        lbl1 = QLabel("Automated Total Coliform Test", self) # Creates a label object
        lbl2 = QLabel("Please connect probe to proceed")

        btn1 = QPushButton("Exit", self) # Creates a pushbutton object

        btn1.setStyleSheet("background-color: #0D47A1; color: #EEEEEE; font-family: Sanserif; font: 20px") # Set style of buton

        lbl1.setStyleSheet("color: #4FC3F7; font: 30px; font-family: Sanserif") # Set style of label
        lbl1.setAlignment(Qt.AlignHCenter) # Align the label to center

        lbl2.setStyleSheet("color: #4FC3F7; font : 20; font-family: Sanserif")
        lbl2.setAlignment(Qt.AlignHCenter)

        btn1.clicked.connect(self.btn1Action) # Add an onclick listener to the button pointing to btn1Action

        self.vbox.addWidget(lbl1) # Add the label to the window
        self.vbox.addWidget(lbl2) # Add the label to the window
        self.vbox.addWidget(btn1) # Add the button to the window

    def InitWorker(self):
        self.thread = QThread(parent=self) # Creates a new thread
        self.worker = Worker1(self.arduino) # Creates a new worker passing arduino listener

        self.stop_signal.connect(self.worker.stop) # Set the stop_signal of this class to point to worker's stop function
        self.worker.moveToThread(self.thread) # Move the worker to the thread

        self.worker.probeDetected.connect(self.NextPage) # Set the probeDetected signal of the worker class to point to NextPage function

        self.worker.finished.connect(self.thread.quit)  # connect the workers finished signal to stop thread
        self.worker.finished.connect(self.worker.deleteLater)  # connect the workers finished signal to clean up worker
        self.thread.finished.connect(self.thread.deleteLater)  # connect threads finished signal to clean up thread
        self.thread.finished.connect(self.worker.stop) # connect threads finished signal to stop the worker

        self.thread.started.connect(self.worker.do_work) #  when the thread starts, the worker will start its loop

        self.thread.start() # Starts the thread

    def keyPressEvent(self, event): # Debugging purposes only dont mind delete after
        if event.key() == Qt.Key_B:
            self.NextPage()

    def btn1Action(self): # Terminates the program when button is pressed
        sys.exit()

    def NextPage(self): # Function that switches the window to the next page
        self.switch_next.emit(self)


class ReadPage(Window):
    switch_next = pyqtSignal(QWidget) # signal to switch to next page

    def __init__(self): # Constructor for ReadPage
        super().__init__() # Initializes the constructor of Window calss
        self.InitWindow() # Initialize window
        self.InitLayout() # Initialize Layout
        self.InitComponents() # Initialize Components
        self.show() # Show the window

    def InitComponents(self): # Initializecomponents
        lbl1 = QLabel("Please place sample into the probe") # Creates a label
        lbl1.setStyleSheet("color: #4FC3F7; font-family: Sanserif; font: 25px")
        lbl1.setAlignment(Qt.AlignHCenter)
        lbl2 = QLabel(self) # set a placeholder for the GIF
        lbl2.setAlignment(Qt.AlignHCenter)
        lbl3 = QLabel("""
        After placing the sample into the probe, 
        press the Get Reading button to start testing""")
        lbl3.setAlignment(Qt.AlignHCenter)
        lbl3.adjustSize() # Adjust size of lbl3
        lbl3.setStyleSheet("color: #FAFAFA; font-family: Sanserif; font: 15px")

        movie = QMovie(self.userpath + '/PycharmProjects/Germz/anim.gif') # Loads the GIF
        movie.setScaledSize(QtCore.QSize(150, 150))

        lbl2.setMovie(movie) # Set the GIF to show in lbl2

        movie.start() # Starts the GIF animation

        btn1 = QPushButton("Get Reading", self)

        btn1.setStyleSheet("background-color: #0D47A1; color: #FAFAFA; font-family: Sanserif; font: 20px")

        btn1.clicked.connect(self.btn1Action)

        self.vbox.addWidget(lbl1) # Adds the lbl1 to the layout
        self.vbox.addWidget(lbl2) # Adds the lbl2 to the layout
        self.vbox.addWidget(lbl3) # Same lang to lahat blablablabla dwele ya mi kabesa
        self.vbox.addWidget(btn1)

    def btn1Action(self): # Function to switch to next page
        self.switch_next.emit(self)


class TestPage(Window): # Third page of program inheriting from class Window

    def __init__(self): # Constructor of the third page
        super().__init__() # Starts the constructor of Window
        self.table = None  # Table for the testpage
        self.InitWindow() # Initializes the window
        self.InitLayout() # Initializes the layout
        self.InitComponents() # Initializes the components

        self.show() # Show the window

    def InitComponents(self):
        lbl1 = QLabel("TCT Data Acquisition...")
        lbl1.setStyleSheet("color: #4FC3F7; font-family: Sanserif; font: 25px")
        lbl1.setAlignment(Qt.AlignHCenter)

        self.table = QTableWidget(self) # Create a new table
        self.table.setColumnCount(6) # Set column number to 6
        self.table.setHorizontalHeaderLabels(['100hz', '1Khz', '2Khz', '15Khz', '50Khz', '80Khz']) # Set label of the horizontal columns
        self.table.verticalHeader().setVisible(True) # Set vertical header to visible
        self.table.setRowCount(2)
        self.table.setVerticalHeaderLabels(['Average Voltage', 'Impedance']) # Set vertical label
        self.table.horizontalHeader().setStretchLastSection(True) # Stretch the headers
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers) # Set the table to be non-editable
        self.table.resizeColumnsToContents() # Resize the columns to fit the contents of the table

        self.table.setStyleSheet("background-color: #212121; font : 15px; font-family : Sanserif; color : gray;") # Set style of the table

        self.vbox.addWidget(lbl1) # add label to layout
        self.vbox.addWidget(self.table) # Add table to layout


class Controller:
    def __init__(self): # Constructor for window switcher
        # self.arduino = SerialListener().start() # Starts the serial listener
        self.StartPage = None # First page
        self.ReadPage = None # Second page
        self.TestPage = None # Third page

    def show_start(self, prev_window): # Show the start page (first window)
        if prev_window is not None: # if there is a previous window
            prev_window.hide() # hide the previous window
        # self.StartPage = StartPage(self.arduino) # pass startpage with the arduino listener
        self.StartPage = StartPage(None) # Debugging (Delete after)
        self.StartPage.switch_next.connect(self.show_read) # Connect the switch_next signal of the start page to show_read function

    def show_read(self, prev_window): # Show the read page (second window)
        if prev_window is not None: # if there is a previous window
            prev_window.hide() # hide the previous window
        self.ReadPage = ReadPage() # create the readpage window
        self.ReadPage.switch_next.connect(self.show_test) # connect the switch next signal of the read page to show the test function

    def show_test(self, prev_window): # Shiw tge test page
        if prev_window is not None: #If there is a previous window
            prev_window.hide() # Hide the previous window
        self.TestPage = TestPage() # Show the test page



if __name__ == "__main__": # If the program starts this file
    app = QApplication(sys.argv) # Create an application object
    controller = Controller() # Start the controller class
    controller.show_start(None) # show the start page
    sys.exit(app.exec()) # Terminate the program when user exits ii.