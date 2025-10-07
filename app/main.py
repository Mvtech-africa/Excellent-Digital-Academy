from flask import Blueprint, render_template
from flask_login import login_required , current_user
from . import model
import os

main = Blueprint('main', __name__)



@main.route('/')
def index():
    return render_template('index.html')



@main.route('/profile')
@login_required
def Profile():
    user_profile = model.Profile.query.filter_by(user_id=current_user.id).first()
    return render_template('profile.html', profile=user_profile)




@main.route('/manage-user')
def ManageUser():
    return render_template('manage-users.html')




@main.route('/dashboard')
@login_required
def Dashboard():
    return render_template('dashboard.html')  


  
@main.route('/viewcourse')
@login_required 
def Viewcourse():
    return render_template('view-course.html')     

