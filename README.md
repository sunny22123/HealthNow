# HealthNow
HealthNow allows you to find healthcare providers in Pittsburgh, Pennsylvania.  

![Image showing four windows of the app. Top left is the Google Maps Query app. Top right is the Welcome window. Bottom left is the Healthcare Provider Map Generator window. Bottom middle is the Healthcare Resource Search System.](static/img/app.jpg "HealthNow Interfaces")

## Motivation
Finding suitable care nearby you is difficult. The goal of HealthNow is to reduce the time and effort needed to do so.
HealthNow is a suite of tools, and this particular tool helps you search for relevant health providers nearby.

## Description
You can search for dentists, doctors, and physical therapists within 3 miles radius. Our tool will give you
a couple of options with their contact information. Our tool uses the Python implementation of the Google Maps
Places V1 API and gives you the most up-to-date information about health providers near you. We have designed
our tool to be a lightweight application before publishing it to the web. 

## Getting Started
### Installation
You can download the package directly by clicking the green Code button and clicking Download Zip in Github.

If you have git installed, you can enter the following command in your terminal:

```
git clone https://github.com/jeffkwang/HealthNow.git
```

### Dependencies
Python installation - if you don't have Python installed, visit https://www.python.org/downloads/ to retrieve
and install Python 3.12.7.

#### Windows
All package dependencies are located in the requirements.txt file. To load the file on a Windows
computer, go to your terminal, navigate to the directory, and enter the commands:

```
python -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt
```

#### Mac
For Mac users, you can enter the commands:

```
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

### API Key
An API key is not provided. You need a Maps Platform API Key, not a Places API Key. For instructions on obtaining
credentials, visit https://developers.google.com/maps/documentation/places/web-service/cloud-setup.

Afterwards, create a text file called API_KEY in the root directory and input:
```
{
    "maps_api_key" : <your key>
}
```

### Executing the program
Our main file is the welcome.py file. To run the program, enter the command:

```
python welcome.py
```

### Troubleshooting
For any troubleshooting, contact jeffwang@andrew.cmu.edu

## Authors
Jeff K Wang - jeffwang - <jeffwang@andrew.cmu.edu>\
Nora Ngo - nngongoc - <nngongoc@andrew.cmu.edu>\
Sunny Lee - hsiangyl - <hsiangyl@andrew.cmu.edu>\
Sri Bhamidipati  - srib - <srib@andrew.cmu.edu>

## Version History
- 0.1
    - Initial Release

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgements
Thank you to Mr. John Ostlund for curating the content for 95-888 - Data Focused Python.
