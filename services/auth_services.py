import json, os, datetime, uuid
# import services.admin_services as admin_services
import hashlib


# Load the existing users from the file
def load_users():
    file_name = 'users.json'

    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        with open(file_name, 'r') as json_file:
            try:
                data = json.load(json_file)  # Load existing data
                if not isinstance(data, list):  # Ensure it's a list
                    data = [data]
            except json.JSONDecodeError:
                data = []  # Handle corrupt or empty JSON files
        return data
    else:
        return []  # If file doesn't exist or is empty, return an empty list

loaded_users = load_users()

# Login logic
def login(username, password):
    users = loaded_users
    for data in users:
        if data.get('user_name') == username and data.get('password') == hashpassword(password):
            print('User has an account')
            return True  # Login successful
    print('Invalid username or password')
    return False  # Invalid credentials


# Create new user
def create_user(first_name, last_name, user_name, email, phone_number, password):
    # Check if the username already exists
    users = loaded_users
    for data in users:
        if data.get('user_name') == user_name:
            print('Username already taken. Please choose a different username.')
            return

    # If username is available, create the user
    user_id = generate_user_id()
    date = datetime.datetime.now()
    new_user = {
        "user_id": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "user_name": user_name,
        "email": email,
        "phone": phone_number,
        "password": hashpassword(password),
        "current_data_time": date.strftime("%c"),
        "isDriver": False
    }

    # Save the new user details to the file
    save_details_to_database(new_user)

    print(f'User created successfully with username: {user_name}')


def hashpassword(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Generate unique user ID
def generate_user_id():
    user_id = str(uuid.uuid1())
    return user_id


# Save user details to the database (users.json)
def save_details_to_database(user_details):
    file_name = 'users.json'

    # Load existing data from the file
    data = loaded_users

    # Append the new user details to the data list
    data.append(user_details)

    # Write the updated data back to the file
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print('User details saved successfully')


# 

# Example usage
# To create a new user:
# create_user('Tony', 'John', 'TonyJ', 'Tony@gmail.com', '08028834967', 'Password')

# # To login with a username and password:
# login('TonyJ', 'Password')
