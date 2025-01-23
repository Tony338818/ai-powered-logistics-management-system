import json
import os

# users
def load_users():
    """Loads user data from a JSON file."""
    try:
        with open("users.json", "r") as f:
            users_data = json.load(f)
            return users_data
    except FileNotFoundError:
        print("user data file not found. Creating a new file.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON. The file might be corrupted.")
        return []
    

def update_user_details(user_id, updates):
    user_data = load_users()
    for index, data in enumerate(user_data):
        if data.get("user_id") == user_id:
            user_data[index].update(updates)
            save_user_data(user_data)
            print(f"User details for {user_id} updated successfully.")
            return  # Exit the loop after updating
    else:
        print(f"User ID {user_id} not found.")


def save_user_data(data):
    """Saves tracking data to a JSON file."""
    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)


def remove_user(user_id):
    """Removes a tracking ID from the tracking data."""
    user_data = load_users()
    for index, data in enumerate(user_data):
        if data.get("user_id") == user_id:
            del user_data[index]
            save_user_data(user_data)
            print(f"Tracking ID {user_id} has been removed.")



# shared services for shipment
file_name = 'package_details.json'

# Load tracking data from the JSON file
def load_shipping_data():
    """Loads tracking data from a JSON file."""
    try:
        with open("package_details.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Tracking data file not found. Creating a new file.")
        return []

def save_shipping_data(data):
    """Saves tracking data to a JSON file."""
    with open("package_details.json", "w") as f:
        json.dump(data, f, indent=4)  

def update_shipping_details(tracking_id, updates):
    shipping_data = load_shipping_data()
    for index, data in enumerate(shipping_data):
        if data.get("tracking_id") == tracking_id:
            shipping_data[index].update(updates)
            save_shipping_data(shipping_data)
            print(f"Tracking details for {tracking_id} updated successfully.")
            return  # Exit the loop after updating
    else:
        print(f"Tracking ID {tracking_id} not found.")

def remove_shipment(tracking_id):
    """Removes a tracking ID from the tracking data."""
    tracking_data = load_shipping_data()
    for index, data in enumerate(tracking_data):
        if data.get("tracking_id") == tracking_id:
            del tracking_data[index]
            save_shipping_data(tracking_data)
            print(f"Tracking ID {tracking_id} has been removed.")

# # # sample usage
# # load_users()
# # update_users('d6cc087e-c447-11ef-817d-ccd9ac1c0538')
# # remove_user('d6cc087e-c447-11ef-817d-ccd9ac1c0538')
# # track_shipment('a553b1ac-c3cb-11ef-af06-ccd9ac1c0538')
# new_values = {
#     "first_name": "Ben",
#     "last_name": "Eki",
#     "user_name": "BenE",
#     "email": "ben@example.com"
# }

# # Call the function with the user ID and updates
# update_user_details("fdfdeb9c-c485-11ef-9832-ccd9ac1c0538", new_values)

# Define the updates as a dictionary
new_shipping_values = {
    "status": "In Transit",
    "current_location": "Lagos, Nigeria",
    "estimated_time": "2024-12-30 15:00:00"
}

# Call the function with the tracking ID and updates
update_shipping_details("123456789ABC", new_shipping_values)
