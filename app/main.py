from flask import Blueprint, render_template

main = Blueprint('main', __name__)



@main.route('/')
def index():
    return render_template('index.html')



@main.route('/profile')
def Profile():
    return render_template('profile.html')



@main.route('/manage-user')
def ManageUser():
    return render_template('manage-users.html')




@main.route('/dashboard')
def Dashboard():
    return render_template('dashboard.html')  


    
@main.route('/viewcourse')
def Viewcourse():
    return render_template('view-course.html')     
