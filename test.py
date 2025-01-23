from flask import Flask, render_template, request, redirect, url_for, flash
import json
import hashlib
from services import shared_services as ss

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

# Load users (drivers) from the JSON file
def load_users():
    """Loads user data from a JSON file."""
    try:
        with open("drivers.json", "r") as f:
            users_data = json.load(f)
            return users_data
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

# Hash password using SHA-256
def hashpassword(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def home():
    return render_template('driver/drivers_login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    drivers_data = load_users()

    for driver in drivers_data:
        if driver['user_name'] == username and driver['password'] == hashpassword(password):
            # Redirect to the driver's dashboard after successful login
            return redirect(url_for('driver_dashboard', driver_id=driver['driver_id']))

    # If login failed
    flash("Invalid username or password")
    return redirect(url_for('home'))

@app.route('/driver_dashboard/<driver_id>')
def driver_dashboard(driver_id):
    # Get the driver data from the loaded users
    drivers_data = load_users()
    shipping_data = ss.load_shipping_data()  # Fetch shipping data using shared services
    driver_info = None
    
    # Find the driver with the given ID
    for driver in drivers_data:
        if driver['driver_id'] == driver_id:
            driver_info = driver
            break
    
    if driver_info is None:
        flash("Driver not found!")
        return redirect(url_for('home'))

    # Pass driver data and shipping data to the template
    return render_template('driver/drivers.html', driver_info=driver_info, shipping_data=shipping_data)

if __name__ == '__main__':
    app.run(debug=True)
