import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HealthNow: Find suitable healthcare providers")
        self.setWindowIcon(QIcon("./static/img/favicon-sm.png"))
        self.setGeometry(100, 100, 400, 250)

        # Create main widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Welcome message
        welcome_label = QLabel("Welcome to HealthNow")
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)

        # Button to open Healthcare Provider Map Generator
        map_button = QPushButton("Open Healthcare Provider Map Generator")
        map_button.clicked.connect(self.open_map_generator)
        layout.addWidget(map_button)

        # Button to open Healthcare Resource Search System
        search_button = QPushButton("Open Healthcare Resource Search System")
        search_button.clicked.connect(self.open_search_system)
        layout.addWidget(search_button)
        
        # New button for Time Search
        Maps_search_button = QPushButton("Open Google Maps Query")
        Maps_search_button.clicked.connect(self.open_gmaps_search)
        layout.addWidget(Maps_search_button)

    def open_map_generator(self):
        from map import HealthcareProviderMapGenerator
        self.map_app = HealthcareProviderMapGenerator()
        self.map_app.show()

    def open_search_system(self):
        from searchHospital import HealthcareResourceSearchSystem
        self.search_app = HealthcareResourceSearchSystem()
        self.search_app.show()

    def open_gmaps_search(self):
        import subprocess
        subprocess.Popen([sys.executable, "gmaps_search/app.py"])

def main():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    welcome_window = WelcomeWindow()
    welcome_window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()