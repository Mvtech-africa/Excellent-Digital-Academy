from flask import Blueprint, render_template
from flask_login import login_required , current_user
from sqlalchemy.orm import joinedload
from . import model
import os
from app import db
main = Blueprint('main', __name__)



@main.route('/')
def index():
    return render_template('index.html')



@main.route('/profile')
@login_required
def Profile():
    user_profile = model.Profile.query.filter_by(user_id=current_user.id).first()
    return render_template('profile.html', profile=user_profile)


@main.route('/profile/<int:user_id>')
def view_profile(user_id):
    user = model.User.query.options(joinedload(model.User.profile)).get_or_404(user_id)
    return render_template('view-profile.html', user=user)

@main.route('/manage-user', methods=['GET'])
def manage_user():
    users = model.User.query.options(db.joinedload(model.User.profile)).all()
    return render_template('manage-users.html', users=users)



@main.route('/dashboard')
@login_required
def Dashboard():
    return render_template('dashboard.html')  



@main.route('/viewcourse')
@login_required 
def Viewcourse():
    return render_template('view-course.html')     





@main.route('/courseupload')
def Courseupload():
    return render_template('course-upload.html') 



@main.route('/updatecourse')
def Updatecourse():
    return render_template('update-course.html') 


    

@main.route('/verifycert')
def Verifycert():
    return render_template('verify-cert.html') 




@main.route('/addcontent')
def Addcontent():
    return render_template('add-content.html') 



    
@main.route('/addcontenttitle')
def Addcontenttitle():
    return render_template('add-c-title.html') 



@main.route('/certprofile')
def Certprofile():
    return render_template('cert-profile.html') 



@main.route('/viewcert')
def viewcert():
    return render_template('view-cert.html') 