from flask import Blueprint, render_template
from flask_login import login_required
from . import model
main = Blueprint('main', __name__)

# Configuration

UPLOAD_FOLDER = 'app/static/uploads/avatars'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file_size(file):
    """Check if file size is within limit"""
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Reset file pointer
    return file_size <= MAX_FILE_SIZE

@main.route('/')
def index():
    return render_template('index.html')



@main.route('/profile')
@login_required
def Profile():
    
    return render_template('profile.html')



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


