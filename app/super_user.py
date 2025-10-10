from flask import Blueprint

super_user = Blueprint('super_user', __name__)

@super_user.route('/admin/dashboard')
def admin_dashboard():
    return "Welcome to the admin dashboard!"
