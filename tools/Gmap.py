import googlemaps
from datetime import datetime

import os
from dotenv import load_dotenv
load_dotenv()

def get_directions(api_key, origin, destination, mode="driving", departure_time=None):
    gmaps = googlemaps.Client(key=api_key)

    try:
        directions_result = gmaps.directions(
            origin,
            destination,
            mode=mode,
            departure_time=departure_time
        )

        if directions_result:
            return directions_result[0]['legs'][0]['steps']
        else:
            print("No directions found.")
            return None

    except Exception as e:
        print(f"Error getting directions: {e}")
        return None

def print_directions(steps):
    if steps:
        for i, step in enumerate(steps, start=1):
            print(f"Step {i}: {step['html_instructions']} ({step['distance']['text']})")


def format_directions(steps):
    directions=[]
    if steps:
        for i, step in enumerate(steps, start=1):
            directions.append(f"Step {i}: {step['html_instructions']} ({step['distance']['text']})")
    return directions

def findDirections(start_loc: str, end_loc:str, means:str) -> str:
    """Useful to get the directions from current location to destination. Means of transport can only be driving, walking, bicycling, or transit. If not specifed, clarify with user
    :params start_loc: starting location
    :params end_loc: destination
    :params means: means of transport
    :returns: directions from start_loc to end_loc
    """
    directions = get_directions(os.getenv('GOOGLEMAPS_API_KEY'), start_loc, end_loc, mode=means, departure_time=None)
    formatted_directions= format_directions(directions)
    return formatted_directions