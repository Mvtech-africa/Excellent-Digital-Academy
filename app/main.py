from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required , current_user
from sqlalchemy import text
from sqlalchemy.orm import joinedload
from .model import User, Profile, Role
import os
from app import db
main = Blueprint('main', __name__)



@main.route('/')
def index():
    return render_template('index.html')



@main.route('/profile')
@login_required
def profile():
    user_profile = Profile.query.filter_by(user_id=current_user.id).first()
    return render_template('profile.html', profile=user_profile, Role=Role)


@main.route('/profile/<int:user_id>')
def view_profile(user_id):
    user = User.query.options(joinedload(User.profile)).get_or_404(user_id)
    return render_template('view-profile.html', user=user)

@main.route('/manage-user', methods=['GET'])
def manage_user():
    users = User.query.options(db.joinedload(User.profile)).all()
    return render_template('manage-users.html', users=users, Role=Role)



@main.route('/dashboard')
@login_required
def Dashboard():
    return render_template('dashboard.html')  





    

@main.route('/verifycert')
def Verifycert():
    return render_template('verify-cert.html') 




@main.route('/addcontent')
def Addcontent():
    return render_template('add-content.html') 



    
@main.route('/addcontenttitle')
def Addcontenttitle():
    return render_template('add-c-title.html') 

@main.route('/update_role/<int:user_id>', methods=['POST'])
@login_required
def update_role(user_id):
    # 🧠 Only admins can update roles
    if current_user.role != Role.ADMIN:
        return jsonify({"error": "Permission denied"}), 403

    data = request.get_json()
    new_role = data.get("role")

    # ✅ Ensure the role is valid
    if new_role not in [role.value for role in Role]:
        return jsonify({"error": "Invalid role"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # ✅ Update the role safely
    user.role = Role(new_role)
    db.session.commit()

    return jsonify({"message": "Role updated successfully", "role": new_role}), 200

@main.route('/certprofile')
def Certprofile():
    return render_template('cert-profile.html') 



@main.route('/viewcert')
def viewcert():
    return render_template('view-cert.html') 