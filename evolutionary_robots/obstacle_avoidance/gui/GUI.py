from PyQt5.QtCore import pyqtSignal, Qt, QCoreApplication
from PyQt5.QtWidgets import QMainWindow
from gui.form import Ui_TrainWindow, Ui_TestWindow
from gui.widgets.logoWidget import LogoWidget

# Test Window
class MainWindow(QMainWindow, Ui_TestWindow):

    updGUI=pyqtSignal()
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.logo = LogoWidget(self)
        self.logoLayout.addWidget(self.logo)
        self.logo.setVisible(True)
        self.display_stats = False
        
        self.clickedButton = False

        self.bestButton.clicked.connect(self.bestClicked)
        
    def updateGUI(self):
        pass
            
    def bestClicked(self):
        generation = int(self.input_generation_2.value())
        self.algorithm.run_state = str(generation)
        self.display_stats = True
        if(self.clickedButton == False):
        	self.algorithm.play()
        	self.clickedButton = True
        else:
        	self.algorithm.select_individual()
    	
    def update_plot(self):
    	self.plot.update_image()

    def setAlgorithm(self, algorithm):
        self.algorithm=algorithm
        _translate = QCoreApplication.translate
        self.input_generation_2.setMaximum(self.algorithm.latest_generation - 1)
        self.out_of_generation_2.setText(_translate("MainWindow", " / " + str(self.algorithm.latest_generation - 1)))

    def getAlgorithm(self):
        return self.algorithm

    def closeEvent(self, event):
        self.algorithm.kill()
        event.accept()
