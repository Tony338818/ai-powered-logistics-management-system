import json
import os
# import shared_services as ss

file_name = 'package_details.json'

def load_tracking_data():
    """Loads tracking data from a JSON file."""
    try:
        with open(file_name, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Tracking data file not found. Creating a new file.")
        return []

def save_tracking_data(data):
    """Saves tracking data to a JSON file."""
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)


def track_package(tracking_id):
    """Tracks a package by its tracking ID."""
    tracking_data = load_tracking_data()
    for data in tracking_data:
        if data.get("shipping_id") == tracking_id:
            return {
                "status": data.get("status", "Status not available"),
                "current_location": data.get("current_location", "Location not available"),
                "eta": data.get("estimated_time", "ETA not available")
            }
    return None

def view_status(tracking_data):
    """Views the current status of a package."""
    status = tracking_data.get("status", "Status not available")
    print(f"Package Status: {status}")
    return status

def view_live_location(tracking_data):
    """Views the live location of a package."""
    location = tracking_data.get("current_location", "Location not available")
    print(f"Live Location: {location}")
    return location

def get_estimated_time(tracking_data):
    """Views the estimated time of arrival for a package."""
    eta = tracking_data.get("estimated_time", "ETA not available")
    print(f"Estimated Time of Arrival: {eta}")
    return eta

def check_tracking_id(tracking_id, tracking_data):
    """Checks for a valid tracking ID and displays details."""
    print(f"Tracking details for {tracking_id}:")
    view_status(tracking_data)
    view_live_location(tracking_data)
    get_estimated_time(tracking_data)


track_package('e1bdeea6-c4bf-4960-86a0-6eba5a097b5e')