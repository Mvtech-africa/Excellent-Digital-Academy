from flask import Blueprint, render_template, redirect, url_for, request, flash,current_app
from flask_login import login_user, logout_user, login_required, current_user
import re
import os
from werkzeug.utils import secure_filename
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.model import User, Profile
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

auth = Blueprint('auth', __name__)
# Password regex: At least one letter, one number, one special character, and min length 8
#PASSWORD_REGEX = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&^])[A-Za-z\d@$!%*#?&^]{8,}$'
# At least one alphabet (A-Z or a-z)
LETTER_REGEX = r'.*[A-Za-z].*'

# At least one digit (0-9)
NUMBER_REGEX = r'.*\d.*'

# At least one special character (@$!%*#?&^)
SPECIAL_CHAR_REGEX = r'.*[@$!%*#?&^].*'

# Minimum 8 characters total
LENGTH_REGEX = r'.{8,}'


limiter = Limiter(
    key_func=get_remote_address,
    app=None,  # Will be set when blueprint is registered
    storage_uri="memory://"
)


# Configuration
UPLOAD_FOLDER = 'app/static/images/avatars'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
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

@auth.before_app_request
def initialize_limiter():
    if not limiter.enabled:
        limiter.init_app(current_app)


@auth.route('/signIn', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def signIn():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')  # ✅ Fixed
            return redirect(next_page or url_for('main.Profile'))
            
        else:
            flash('Invalid email or password. Please try again.', 'error')
            return redirect(url_for('auth.signIn'))

    return render_template('signin.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        phone = request.form.get('phone')
        tos = request.form.get('tos') == 'on'  # ✅ Fixed checkbox handling

        # Must accept Terms of Service
        if not tos:
            flash('You must agree to the Terms of Service.', 'error')
            return redirect(url_for('auth.signup'))

        # Check for missing fields
        if not (first_name and last_name and email and password and phone):
            flash('All fields are required.', 'error')
            return redirect(url_for('auth.signup'))

        # Password match check
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('auth.signup'))
        
        # Validate password strength
        if not re.match(LETTER_REGEX, password):
            flash('Password must  lowercase and uppercase letters.', 'error')
            return redirect(url_for('auth.signup'))
        elif not re.match(NUMBER_REGEX, password):
            flash('Password must contain at least one number.', 'error')
            return redirect(url_for('auth.signup'))
        elif not re.match(SPECIAL_CHAR_REGEX, password):
            flash('Password must contain at least one special character (@$!%*#?&^).', 'error')
            return redirect(url_for('auth.signup'))
        elif not re.match(LENGTH_REGEX, password):
            flash('Password must be at least 8 characters long.', 'error')
            return redirect(url_for('auth.signup'))
    
        
        

        # Email uniqueness check
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists. Please login.', 'error')
            return redirect(url_for('auth.signIn'))

        # Create new userS
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=generate_password_hash(password),
            phone=phone,
            tos=tos  # ✅ Save to DB
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('auth.signIn'))
        except Exception as e:
            db.session.rollback()
            logging.error("DB Error:", e)
            flash("Database error: " + str(e), "error")
            return redirect(url_for("auth.signup"))


    return render_template('signup.html')


@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # Here you would normally send an email with a reset link
            flash('Password reset instructions have been sent to your email.', 'success')
        else:
            flash('Email not found. Please check and try again.', 'error')
        return redirect(url_for('auth.forgot_password'))
    return render_template('forgot-password.html')




@auth.route('/update-profile', methods=['POST'])  # ✅ Remove GET, only POST
@login_required
def update_profile():
    """Update user profile (bio and avatar)"""
    
    
    bio = request.form.get('bio', '').strip()
    state = request.form.get('state', '').strip()
    country = request.form.get('country', '').strip()
    address = request.form.get('address', '').strip()
    avatar = request.files.get('avatar')
    
    # Get existing profile or prepare to create new one
    user_profile = Profile.query.filter_by(user_id=current_user.id).first()
    
    # Validate bio length
    if bio and len(bio) > 500:
        flash('Bio must be less than 500 characters.', 'error')
        return redirect(url_for('main.profile'))  # ✅ Changed
    
    avatar_url = None
    
    # Handle avatar upload
    if avatar and avatar.filename:
        # Validate file type
        if not allowed_file(avatar.filename):
            flash('Invalid file type. Only PNG, JPG, JPEG, GIF, and WEBP are allowed.', 'error')
            return redirect(url_for('main.profile'))  # ✅ Changed
        
        # Validate file size
        if not validate_file_size(avatar):
            flash('File size must be less than 5MB.', 'error')
            return redirect(url_for('main.profile'))  # ✅ Changed
        
        # Delete old avatar if it exists
        if user_profile and user_profile.avatar_url:
            old_file_path = os.path.join('app', user_profile.avatar_url.lstrip('/'))
            if os.path.exists(old_file_path):
                try:
                    os.remove(old_file_path)
                except OSError as e:
                    print(f"Error deleting old avatar: {e}")
        
        # Secure the filename and make it unique with timestamp
        from datetime import datetime
        filename = secure_filename(avatar.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{current_user.id}_{timestamp}_{filename}"
        
        # Ensure upload directory exists
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Save the file
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        avatar.save(file_path)
        
        # Store relative path for URL
        avatar_url = f"/static/images/avatars/{unique_filename}"
    
    # Update or create profile
    try:
        if user_profile:
            # Update existing profile
            if bio is not None:
                user_profile.bio = bio if bio else None
            if state:
                user_profile.state = state if state else None
            if country:
                user_profile.country = country if country else None
            if avatar_url:
                user_profile.avatar_url = avatar_url
            if address:
                user_profile.address = address
        else:
            # Create new profile
            user_profile = Profile(
                user_id=current_user.id,
                bio=bio if bio else None,
                state=state if state else None,
                country=country if country else None,
                avatar_url=avatar_url,
                address = address if address else None
            )
            db.session.add(user_profile)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while updating your profile. Please try again.', 'error')
        logging.error(f"Profile update error: {e}")
    
    # ✅ IMPORTANT: Must redirect to a GET route
    return redirect(url_for('main.profile'))  # NOT back to update_profile!

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'error')
    return redirect(url_for('main.index'))
