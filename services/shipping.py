import uuid
import datetime
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import os
import json

# Shared services for shipment
file_name = 'package_details.json'

def load_shipping_data():
    """Loads tracking data from a JSON file."""
    if not os.path.exists(file_name):
        print("Tracking data file not found. Creating a new file.")
        return []  # Return an empty list if the file doesn't exist

    try:
        with open(file_name, "r") as f:
            data = f.read().strip()
            if not data:
                return []  # Return an empty list if the file is empty
            return json.loads(data)
    except json.JSONDecodeError:
        print("Error decoding JSON. The file may be corrupted or empty.")
        return []  # Return an empty list if JSON is invalid


def save_shipping_data(data):
    """Saves tracking data to a JSON file."""
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)

def update_shipping_details(shipping_id, updates):
    """Updates the shipping details based on shipping ID."""
    shipping_data = load_shipping_data()
    for index, data in enumerate(shipping_data):
        if data.get("shipping_id") == shipping_id:
            shipping_data[index].update(updates)
            save_shipping_data(shipping_data)
            print(f"Tracking details for {shipping_id} updated successfully.")
            return  # Exit the loop after updating
    else:
        print(f"Tracking ID {shipping_id} not found.")

def remove_shipment(shipping_id):
    """Removes a shipment by its shipping ID."""
    shipping_data = load_shipping_data()
    for index, data in enumerate(shipping_data):
        if data.get("shipping_id") == shipping_id:
            del shipping_data[index]
            save_shipping_data(shipping_data)
            print(f"Tracking ID {shipping_id} has been removed.")
            return
    print(f"Tracking ID {shipping_id} not found.")

def get_coordinates(location_name):
    """Gets coordinates for a given location name."""
    geolocator = Nominatim(user_agent="sem4project-app/1.0")
    location = geolocator.geocode(location_name)
    if location:
        return (location.latitude, location.longitude)
    else:
        print(f"Could not find coordinates for {location_name}")
        return None

def generate_price(pickup_location, dropoff_location, weight, delivery_method):
    """Calculates the shipping price based on location, weight, and delivery method."""
    pickup_coords = get_coordinates(pickup_location)
    dropoff_coords = get_coordinates(dropoff_location)
    if not pickup_coords or not dropoff_coords:
        print("Could not retrieve coordinates. Price calculation failed.")
        return None

    # Base price per kilometer
    base_rate = 2.0  # $2 per km

    # Weight surcharge per kilogram
    weight_surcharge = 0.5  # $0.5 per kg

    # Delivery method multipliers
    method_multiplier = {
        "standard": 1.0,
        "express": 1.5,
        "same-day": 2.0,
    }

    if delivery_method not in method_multiplier:
        print("Invalid delivery method. Choose from 'standard', 'express', or 'same-day'.")
        return None

    distance = geodesic(pickup_coords, dropoff_coords).kilometers
    base_price = distance * base_rate
    weight_cost = weight * weight_surcharge
    total_price = (base_price + weight_cost) * method_multiplier[delivery_method]

    print(f"The delivery price is: ${total_price:.2f}")
    return total_price

def generate_shipping_id():
    """Generates a unique shipping ID."""
    return str(uuid.uuid4())

def save_details_to_database(s_name, r_name, ship_mode, pickup, drop, weight):
    """Saves shipping details to the database and returns tracking ID and price."""
    shipping_id = generate_shipping_id()
    date = datetime.datetime.now()
    new_date = date + datetime.timedelta(days=2)

    price = generate_price(pickup, drop, weight, ship_mode)
    if price is None:
        print("Failed to create shipment due to invalid data.")
        return None, None

    details = {
        "senders_name": s_name,
        "receivers_name": r_name,
        "shipping_method": ship_mode,
        "pickup_location": pickup,
        "drop_location": drop,
        "shipping_id": shipping_id,
        "price": price,
        "status": "shipped",
        "current_data_time": date.strftime("%c"),
        "estimated_time": new_date.strftime("%c"),
        "current_location": pickup,
    }

    shipping_data = load_shipping_data()
    shipping_data.append(details)
    save_shipping_data(shipping_data)

    print(f"Shipment created successfully with Tracking ID: {shipping_id}")
    return shipping_id, price


def create_shipment(s_name, r_name, pickup, drop, weight, ship_mode):
    """Creates a new shipment by integrating user input and system logic."""
    shipping_id, price = save_details_to_database(s_name, r_name, ship_mode, pickup, drop, weight)
    return shipping_id, price



# create_shipment(
#     s_name="Alice",
#     r_name="Bob",
#     pickup="Lagos",
#     drop="Abuja",
#     weight=12.5,
#     ship_mode='express'
# )

# new_data = {
#      "status": "in transit",
#      "current_location": "cross river"
# }

# update_shipping_details("e929163e-cdb9-42c1-a664-6cd4b1305b80", new_data)

# remove_shipment("e929163e-cdb9-42c1-a664-6cd4b1305b80")
