'''
Date: 10-07-2024
@author: Jeff K Wang
'''
from google.maps import places_v1
from google.api_core.client_options import ClientOptions
import pandas as pd
import json
from google.protobuf.json_format import MessageToDict

def miles_to_meters(miles):
    try:
        return miles * 1_609.344
    except:
        return 0

"""
The googleMapQuery class handles the initialization of the Google Places V1 search client.

Attributes:
    - API key
    - location and services coding schema
    - search function
"""
class googleMapQuery():
    """
    Initialization of the googleMapQuery object obtains the API key, location and services coding schema, and the 
    Google Maps client.
    """
    def __init__(self):
        # load api key
        with open("./API_KEY", "r") as file:
            data = json.load(file)
            self.__API_KEY = data["maps_api_key"]
            options = ClientOptions(api_key = self.__API_KEY)

        # load user input coding schema
        self.__location_options = {"Shadyside": (40.45477962245367, -79.93261498677636),
                    "Squirrel Hill-North": (40.44597423568556, -79.92789391494384),
                    "Squirrel Hill-South": (40.43506983990427, -79.92341536757911),
                    "North Oakland": (40.44843139299627, -79.95150549424802),
                    "South Oakland": (40.4321842041154, -79.9583419476085),
                    "East Liberty": (40.46423220390781, -79.92572956705438),
                    "Friendship": (40.46099669926969, -79.93465627400883)}

        self.__service_options = {"Dental Care": 
                                  {"query": "dentist", "googletype": "dental_clinic"},
                                  "Health Care": 
                                  {"query": "doctor", "googletype": "doctor"},
                                  "Physical Therapy": 
                                  {"query": "physical therapy", "googletype": "physiotherapist"}}
        
        # initialize Google Maps client
        self.__gplaces = places_v1.PlacesClient(client_options=options) 
    
    def search(self, service, location):
        """
        Gets predefined `service and `location values from user. Then, retrieves the coding schema defined 
        above. Creates a request object. Returns response.

        Input: service and location strings
        Output: Places API SearchTextQuery object
        """
        Location = self.__location_options[location]
        latitude = Location[0]; longitude = Location[1]

        query = self.__service_options[service]["query"]
        googletype = self.__service_options[service]["googletype"]
        
        search_request = places_v1.SearchTextRequest(
            text_query = query,
            location_bias = {
                "circle": {
                    "center": {
                        "latitude": latitude,
                        "longitude": longitude,
                    },
                    "radius": miles_to_meters(3)
                }
            },
            included_type = googletype,
            strict_type_filtering = True,
            rank_preference = 0
        )

        search_response = self.__gplaces.search_text(search_request, metadata=[('x-goog-fieldmask', 
                                                                                'places.displayName,places.formattedAddress,places.rating,places.current_opening_hours')])
        return search_response
    
    def to_table(self, response):
        """
        Converts protobuf object to a dictionary. See https://googleapis.dev/python/protobuf/latest/google/protobuf/json_format.html
        
        Input: Search Text Response Object. See https://googleapis.dev/python/places/latest/_modules/google/maps/places_v1/types/places_service.html#SearchTextResponse
        Output: Pandas dataframe
        """
        dict_representation = []

        for place in response.places:
            element = MessageToDict(place.__dict__["_pb"])

            # in case of no data point, then an NA value is substituted            
            if "displayName" in element:
                element["displayName"] = element["displayName"]["text"]
            else:
                element["displayName"] = "NA"

            if "currentOpeningHours" in element:
                element["currentOpeningHours"] = [item.replace('\u202f', ' ').replace('\u2009', ' ') for item in element["currentOpeningHours"]["weekdayDescriptions"]]
            else:
                element["currentOpeningHours"] = "NA"
            
            dict_representation.append(element)
        df = pd.DataFrame(dict_representation)
        cols = list(df.columns.values)
        cols[cols.index('displayName')], cols[0] = cols[0], cols[cols.index('displayName')]
        df = df[cols]
        df.columns = ["PROVIDER", "RATING", "ADDRESS", "HOURS"]
        return df    
    
if __name__ == "__main__":
    import pprint

    placesClient = googleMapQuery()
    response = placesClient.search("Physical Therapy", "Shadyside")
    table = placesClient.to_table(response)
    # pprint.pprint(table.head())
