# Module by Hugo BONNELL

import requests
import pandas as pd

def retrieveDataFromJson(url : str):
    '''
    Retrieve the json data of the given URL.
    '''
    response = requests.get(url)

    if(response.status_code == 200):    
        # Means that we could get the data
        # Parse the JSON
        data = response.json()

        # Extract features
        features = data.get("features", [])

        # Flatten the data into a list of dictionaries
        flattened_data = []
        for feature in features:
            # Combine properties and geometry into a single dictionary
            flattened_dict = feature.get("properties", {})
            geometry = feature.get("geometry", {})
            flattened_dict["geometry"] = geometry
            flattened_data.append(flattened_dict)

        # Create a pandas DataFrame
        dataFrame = pd.DataFrame(flattened_data)

        return dataFrame
    else:
        print("Error: couldn't GET url: ", url)
        return None