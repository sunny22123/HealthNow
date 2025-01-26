'''
Date: 10-07-2024
@author: Jeff K Wang
'''
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QTableView
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice
import search
from dataframe_model import PandasModel

"""
The MainWindow class handles the initialization of the main menu.

Methods:
- loadCustomWidget : private class that loads the UI file from PyDesigner
- showSearchResults : event and data pipeline to the Search Query window
- showWindow : open window
- getWindowState : returns True if the window is open 
"""
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # set window icon
        self.setWindowIcon(QIcon("./static/img/favicon-sm.png"))

        # set window styling: size, title, background
        self.resize(1333, 500)
        self.setWindowTitle("HealthNow: Find suitable healthcare providers")
        self.background = QLabel(self)
        pixmap = QPixmap("./static/img/bg.jpg")
        self.background.setPixmap(pixmap)
        self.background.resize(pixmap.width(), pixmap.height())

        # path to UI file
        self.__main_ui = "./pyside_ui/gui.ui"
        
        # QUiLoader loading
        loader = QUiLoader()
        ui_file = QFile(self.__main_ui)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {self.__main_ui}: {ui_file.errorString()}")
            sys.exit(-1)
        window = loader.load(ui_file, self)
        ui_file.close()

        window.tableView.setVisible(False)

        self.setCentralWidget(window)

        self.__searchbutton = window.searchButton
        self.__serviceQuery = window.service
        self.__locationQuery = window.location
        self.__queryView = window.tableView

        self.searchClient = search.googleMapQuery()
        
    # getter class methods
    def getSearchButton(self):
        return self.__searchbutton
    def getServiceQuery(self):
        return self.__serviceQuery
    def getLocationQuery(self):
        return self.__locationQuery
    
    # search button clicked event handler
    # retrieves service and location inputs
    # converts SearchTextQuery object to a pandas dataframe
    # calls PandasModel to make the table viewable on the QtTableViews widget in the UI
    def on_search_button_clicked(self):
        serviceInput = self.getServiceQuery().currentText()
        locationInput = self.getLocationQuery().currentText()
        df = self.searchClient.to_table( # converts Google Map Places object into a Pandas dataframe
            self.searchClient.search(serviceInput, locationInput) # returns Google Map Places type object
        )
        model = PandasModel(df)
        self.__queryView.setModel(model)
        self.__queryView.setVisible(True) 
        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    search_button = window.getSearchButton()
    search_button.clicked.connect(window.on_search_button_clicked)

    sys.exit(app.exec())