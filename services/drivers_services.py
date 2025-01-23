import json, os, uuid, hashlib, datetime


def load_users():
    """Loads user data from a JSON file."""
    try:
        with open("drivers.json", "r") as f:
            users_data = json.load(f)
            return users_data
    except FileNotFoundError:
        print("User data file not found. Creating a new file.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON. The file might be corrupted.")
        return []

driver_data = load_users()

# Create new driver
def create_driver(first_name, last_name, user_name, email, phone_number, password, vehicle_id, vehicle_plates, vehicle_name_model):
    """Creates a new driver with initial stats."""
    # Check if the username already exists
    users = load_users()
    for data in users:
        if data.get('user_name') == user_name:
            print('Username already taken. Please choose a different username.')
            return

    # If username is available, create the driver
    driver_id = generate_driver_id()
    date = datetime.datetime.now()
    new_driver = {
        "driver_id": driver_id,
        "first_name": first_name,
        "last_name": last_name,
        "user_name": user_name,
        "email": email,
        "phone": phone_number,
        "password": hashpassword(password),
        "current_data_time": date.strftime("%c"),
        "vehicle_id": vehicle_id,
        "vehicle_plates": vehicle_plates,
        "vehicle_name_model": vehicle_name_model,
        # Driver stats
        "stats": {
            "pending_deliveries": 0,
            "deliveries_completed": 0,
            "average_delivery_time": 0,
            "average_rating": 0
        }
    }

    # Save the new driver details to the file
    save_details_to_database(new_driver)

    print(f'Driver created successfully with username: {user_name}')


def hashpassword(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


# Generate unique driver ID
def generate_driver_id():
    """Generates a unique driver ID."""
    return str(uuid.uuid1())


# Save driver details to the database (drivers.json)
def save_details_to_database(driver_details):
    """Saves driver details to the JSON file."""
    file_name = 'drivers.json'

    # Load existing data from the file
    data = load_users()

    # Append the new driver details to the data list
    data.append(driver_details)

    # Write the updated data back to the file
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print('Driver details saved successfully')


# Update driver stats
def update_driver_stats(driver_id, updates):
    """
    Updates the driver's statistics based on their ID.

    Args:
        driver_id (str): The unique ID of the driver.
        updates (dict): A dictionary containing the fields to update and their new values.
    """
    # Load the existing driver data
    drivers = load_users()
    for index, driver in enumerate(drivers):
        if driver.get("driver_id") == driver_id:
            # Update the stats with the provided values
            driver["stats"].update(updates)
            
            # Save the updated driver data back to the file
            with open("drivers.json", "w") as f:
                json.dump(drivers, f, indent=4)
            
            print(f"Stats for driver ID {driver_id} updated successfully.")
            return  # Exit after updating
    else:
        print(f"Driver ID {driver_id} not found.")


def get_driver_details(driver_id):
    drivers_data = driver_data
    for index, data in enumerate(drivers_data):
        if data.get('driver_id') == driver_id:
            print(f"details for {driver_id} retrieved successfully.")
            return drivers_data[index]
        else:
            print(f"driver ID {driver_id} not found.")

# Example usage
# To create a new driver:
# create_driver('Tony', 'John', 'TonyJ', 'Tony@gmail.com', '08028834967', 'Password', 'vehicle_id', 'Ak19300', 'Lexus RX350')

# To update stats for a driver:
# update_driver_stats(
#     driver_id="7fa10e5a-c527-11ef-a47a-ccd9ac1c0538",
#     updates={
#         "pending_deliveries":0,
#         "deliveries_completed": 6,
#         "average_delivery_time":"4 hrs",
#         "average_rating": 4.7
#     }
# )

