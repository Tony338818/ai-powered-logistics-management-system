from flask import Flask, request, redirect, render_template, jsonify, url_for, flash
from services import shipping, tracking, shared_services as ss
from services import auth_services
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/')
def home():
    return render_template('users/index.html')
@app.route('/ship')
def ship():
    return render_template('users/shipping.html')
@app.route('/track')
def track():
    return render_template('users/tracking.html')
@app.route('/service')
def service():
    return render_template('users/tracking.html')
@app.route('/faq')
def faq():
    return render_template('users/tracking.html')

@app.route('/shipping', methods=['POST'])
def process_shipping():
    data = request.json
    senders_name = data.get('sendersName')
    receivers_name = data.get('receiversName')
    pickup_location = data.get('pickupLocation')
    drop_location = data.get('dropLocation')
    package_details = data.get('packageDetails')
    delivery_method = data.get('deliveryMethod')

    if senders_name and receivers_name and pickup_location and drop_location and package_details and delivery_method:
        tracking_id, price = shipping.create_shipment(senders_name, receivers_name, pickup_location, drop_location, 10, delivery_method)
        if tracking_id and price:
            return jsonify({"message": "Shipping processed", "tracking_id": tracking_id, "price": price})
        else:
            return jsonify({"error": "Failed to create shipment due to invalid data"}), 400
    else:
        return jsonify({"error": "All fields are required"}), 400


@app.route('/tracking', methods=['POST'])
def process_tracking():
    data = request.json
    tracking_id = data.get('tracking_id')
    if tracking_id:
        tracking_data = tracking.track_package(tracking_id)
        if tracking_data:
            return jsonify(tracking_data)
        else:
            return jsonify({"status": "Tracking ID not found"}), 404
    else:
        return jsonify({"status": "Tracking ID is required"}), 400



@app.route('/driver_dashboard/<driver_id>')
def driver_dashboard(driver_id):
    # Get the driver data from the loaded users
    drivers_data = ss.load_users()
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


@app.route('/register', methods=['POST'])
def create_user():
    data = request.json

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    user_name = data.get('user_name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    auth_services.create_user(first_name, last_name, user_name, email, phone, password)

# @app.route('/login', methods=['POST'])
# def handle_login():
#     role = request.form['role']
#     email = request.form['email']
#     password = request.form['password']
    
#     # Additional fields based on role
#     if role == 'user':
#         if user_service.authenticate(email, password):
#             return redirect(url_for('user_page'))
#     elif role == 'admin':
#         if admin_service.authenticate(email, password):
#             return redirect(url_for('admin_page'))
#     elif role == 'driver':
#         if drivers_service.authenticate(email, password):
#             return redirect(url_for('driver_page'))
    
#     return "Invalid credentials", 400

@app.route('/user')
def user_page():
    return render_template('user/user_page.html')

@app.route('/admin')
def admin_page():
    return render_template('admin/admin_page.html')

@app.route('/driver')          
def driver_page():
    return render_template('drivers/drivers_page.html')

if __name__ == '__main__':
    app.run(debug=True)
