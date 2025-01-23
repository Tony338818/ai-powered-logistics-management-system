from flask import Flask, render_template, request, redirect, url_for
from services.admin_service import AdminService
from services.user_service import UserService
from services.drivers_service import DriversService

app = Flask(__name__)

# Dummy services for illustration
admin_service = AdminService()
user_service = UserService()
drivers_service = DriversService()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def handle_login():
    role = request.form['role']
    email = request.form['email']
    password = request.form['password']
    
    # Additional fields based on role
    if role == 'user':
        if user_service.authenticate(email, password):
            return redirect(url_for('user_page'))
    elif role == 'admin':
        if admin_service.authenticate(email, password):
            return redirect(url_for('admin_page'))
    elif role == 'driver':
        if drivers_service.authenticate(email, password):
            return redirect(url_for('driver_page'))
    
    return "Invalid credentials", 400

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
