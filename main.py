from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from arduino import SerialListener
import os
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Automated Total Coliform Test"
        self.left = 0
        self.top = 0
        self.width = 480
        self.height = 320
        self.userpath = os.getenv("HOME")
        self.icon = QIcon(self.userpath + '/PycharmProjects/Germz/favicon.jpg')
        self.vbox = QVBoxLayout()
        self.gbox = QGridLayout()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color: #424242")
        self.setWindowIcon(self.icon)
        self.setMaximumHeight(self.height)
        self.setMaximumWidth(self.width)
        self.setMinimumHeight(self.height)
        self.setMinimumWidth(self.width)

    def InitLayout(self):
        self.setLayout(self.vbox)
        self.vbox.setGeometry(QRect(self.left, self.top, self.width, self.height))
        self.vbox.setSpacing(10)


class Worker1(QObject):
    finished = pyqtSignal()  # give worker class a finished signal
    probeDetected = pyqtSignal()

    def __init__(self, arduino, parent=None):
        QObject.__init__(self, parent=parent)
        self.arduino = arduino
        self.continue_run = True

    def do_work(self):
        # while self.continue_run:  # give the loop a stoppable condition
            # self.arduino.resume()
            # reading = self.arduino.read()
            # if reading == "OK":
            #    self.probeDetected.emit()
            #    self.stop()
        # self.reader.pause()
        self.finished.emit()

    def stop(self):
        self.continue_run = False


class StartPage(Window):
    switch_next = pyqtSignal(QWidget)
    stop_signal = pyqtSignal()

    def __init__(self, arduino):
        super().__init__()
        self.arduino = arduino
        self.thread = None
        self.worker = None
        self.InitWindow()
        self.InitLayout()
        self.InitComponents()
        self.InitWorker()
        self.show()

    def InitComponents(self):
        lbl1 = QLabel("Automated Total Coliform Test", self)
        lbl2 = QLabel("Please connect probe to proceed")

        btn1 = QPushButton("Exit", self)

        btn1.setStyleSheet("background-color: #0D47A1; color: #EEEEEE; font-family: Sanserif; font: 20px")

        lbl1.setStyleSheet("color: #4FC3F7; font: 30px; font-family: Sanserif")
        lbl1.setAlignment(Qt.AlignHCenter)

        lbl2.setStyleSheet("color: #4FC3F7; font : 20; font-family: Sanserif")
        lbl2.setAlignment(Qt.AlignHCenter)

        btn1.clicked.connect(self.btn1Action)

        self.vbox.addWidget(lbl1)
        self.vbox.addWidget(lbl2)
        self.vbox.addWidget(btn1)

    def InitWorker(self):
        self.thread = QThread(parent=self)
        self.worker = Worker1(self.arduino)

        self.stop_signal.connect(self.worker.stop)
        self.worker.moveToThread(self.thread)

        self.worker.probeDetected.connect(self.NextPage)

        self.worker.finished.connect(self.thread.quit)  # connect the workers finished signal to stop thread
        self.worker.finished.connect(self.worker.deleteLater)  # connect the workers finished signal to clean up worker
        self.thread.finished.connect(self.thread.deleteLater)  # connect threads finished signal to clean up thread
        self.thread.finished.connect(self.worker.stop)

        self.thread.started.connect(self.worker.do_work)

        self.thread.start()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_B:
            self.NextPage()

    def btn1Action(self):
        sys.exit()

    def NextPage(self):
        self.switch_next.emit(self)


class ReadPage(Window):
    switch_next = pyqtSignal(QWidget)

    def __init__(self):
        super().__init__()
        self.InitWindow()
        self.InitLayout()
        self.InitComponents()
        self.show()

    def InitComponents(self):
        lbl1 = QLabel("Please place sample into the probe")
        lbl1.setStyleSheet("color: #4FC3F7; font-family: Sanserif; font: 25px")
        lbl1.setAlignment(Qt.AlignHCenter)
        lbl2 = QLabel(self)
        lbl2.setAlignment(Qt.AlignHCenter)
        lbl3 = QLabel("""
        After placing the sample into the probe, 
        press the Get Reading button to start testing""")
        lbl3.setAlignment(Qt.AlignHCenter)
        lbl3.adjustSize()
        lbl3.setStyleSheet("color: #FAFAFA; font-family: Sanserif; font: 15px")

        movie = QMovie(self.userpath + '/PycharmProjects/Germz/anim.gif')
        movie.setScaledSize(QtCore.QSize(150, 150))

        lbl2.setMovie(movie)

        movie.start()

        btn1 = QPushButton("Get Reading", self)

        btn1.setStyleSheet("background-color: #0D47A1; color: #FAFAFA; font-family: Sanserif; font: 20px")

        btn1.clicked.connect(self.btn1Action)

        self.vbox.addWidget(lbl1)
        self.vbox.addWidget(lbl2)
        self.vbox.addWidget(lbl3)
        self.vbox.addWidget(btn1)

    def btn1Action(self):
        self.switch_next.emit(self)


class TestPage(Window):

    def __init__(self):
        super().__init__()
        self.InitWindow()
        self.InitLayout()
        self.InitComponents()

        self.show()

    def InitComponents(self):
        lbl1 = QLabel("Coliform 


class Controller:
    def __init__(self):
        # self.arduino = SerialListener().start()
        self.StartPage = None
        self.ReadPage = None
        self.TestPage = None

    def show_start(self, prev_window):
        if prev_window is not None:
            prev_window.hide()
        # self.StartPage = StartPage(self.arduino)
        self.StartPage = StartPage(None)
        self.StartPage.switch_next.connect(self.show_read)

    def show_read(self, prev_window):
        if prev_window is not None:
            prev_window.hide()
        self.ReadPage = ReadPage()
        self.ReadPage.switch_next.connect(self.show_test)

    def show_test(self, prev_window):
        if prev_window is not None:
            prev_window.hide()
        self.TestPage = TestPage()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.show_start(None)
    sys.exit(app.exec())