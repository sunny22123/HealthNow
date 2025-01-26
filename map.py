# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 15:47:38 2024

@author: Nhu Ngo
"""

import sys
import pandas as pd
import folium
import webbrowser
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QComboBox

class HealthcareProviderMapGenerator(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Healthcare Provider Map Generator")
        self.setGeometry(100, 100, 400, 200)

        # Create main widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Create a label
        label = QLabel("Select a provider type:")
        layout.addWidget(label)

        # Create a dictionary mapping display names to worksheet names
        self.worksheet_dict = {
            "Dentists": "google_maps_dentists (clean)",
            "Physical Therapy Clinics": "google_maps_phys_therapy (clean",
            "Clinics": "google_maps_clinics (clean)"
        }

        # Create a dropdown menu for worksheet selection
        self.worksheet_dropdown = QComboBox()
        self.worksheet_dropdown.addItems(list(self.worksheet_dict.keys()))
        self.worksheet_dropdown.setCurrentText("Dentists")  # Set default value
        layout.addWidget(self.worksheet_dropdown)

        # Create a button to generate the map
        generate_button = QPushButton("Generate Map")
        generate_button.clicked.connect(self.generate_map)
        layout.addWidget(generate_button)

        # Create a label to show the status
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

    def create_map(self, worksheet):
        # Load the providers data
        file_path = 'Data/project_prototype.xlsx'
        excel_data = pd.ExcelFile(file_path)

        df = excel_data.parse(worksheet)

        # Extract latitude and longitude from the 'geometry' field
        df['latitude'] = df['geometry'].apply(lambda x: eval(x)['location']['lat'])
        df['longitude'] = df['geometry'].apply(lambda x: eval(x)['location']['lng'])

        # Create a map centered around Pittsburgh (adjust as needed)
        map_center = [40.4431, -79.9235]
        provider_map = folium.Map(location=map_center, zoom_start=12)

        # Add markers to the map for each provider's location
        for idx, row in df.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup="Address: " + row['vicinity'] + "<br>Rating: " + str(row['rating']),
                tooltip=row['name']
            ).add_to(provider_map)

        # Save the map as an HTML file
        map_file = f'{worksheet.split()[0]}_map.html'
        provider_map.save(map_file)
        return map_file

    def generate_map(self):
        selected_display_name = self.worksheet_dropdown.currentText()
        selected_worksheet = self.worksheet_dict[selected_display_name]
        map_file = self.create_map(selected_worksheet)
        self.status_label.setText(f"Map generated: {map_file}")
        webbrowser.open(map_file)

def main():
    app = QApplication(sys.argv)
    window = HealthcareProviderMapGenerator()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()