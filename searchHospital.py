"""
Created on Sun Oct  6 15:47:38 2024

@author: Sunny Lee
"""

import sys
import pandas as pd
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                               QWidget, QPushButton, QComboBox, QTableView, QLabel)
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex

class PandasModel(QAbstractTableModel):
    def __init__(self, dataframe: pd.DataFrame, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._dataframe = dataframe

    def rowCount(self, parent=QModelIndex()) -> int:
        if parent == QModelIndex():
            return len(self._dataframe)
        return 0

    def columnCount(self, parent=QModelIndex()) -> int:
        if parent == QModelIndex():
            return len(self._dataframe.columns)
        return 0

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return str(self._dataframe.iloc[index.row(), index.column()])
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dataframe.columns[section])
            if orientation == Qt.Vertical:
                return str(self._dataframe.index[section])
        return None

class HealthcareResourceSearchSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Healthcare Resource Search System")
        self.setGeometry(100, 100, 800, 600)

        # Load the CSV file
        self.df = pd.read_csv('Data/certificated_board.csv')

        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Create combo box for profession selection
        self.profession_combo = QComboBox()
        self.profession_combo.addItems(self.df.columns[1:])
        main_layout.addWidget(QLabel("Select a profession:"))
        main_layout.addWidget(self.profession_combo)

        # Create search button
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_profession)
        main_layout.addWidget(search_button)

        # Create table view
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        main_layout.addWidget(self.table_view)

    def search_profession(self):
        profession = self.profession_combo.currentText()
        result = self.search_by_profession(profession)
        if result is not None:
            model = PandasModel(result)
            self.table_view.setModel(model)
            self.table_view.resizeColumnsToContents()

    def search_by_profession(self, profession):
        sorted_df = self.df.sort_values(by=profession, ascending=False)
        return sorted_df[['FACILITY NAME', profession]]

if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    window = HealthcareResourceSearchSystem()
    window.show()
    sys.exit(app.exec())

