from flask import Blueprint, render_template, redirect, url_for, request, flash,current_app
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
import re
import os
from werkzeug.utils import secure_filename
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.model import User, Profile
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

auth = Blueprint('auth', __name__)


mail = Mail()
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



# Upload config
UPLOAD_FOLDER = 'app/static/images/avatars'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Ensure folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file_size(file):
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size <= MAX_FILE_SIZE

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
            #flash('Login successful!', 'success')  # ✅ Fixed
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
            # Create a secure token valid for 30 minutes
            token = URLSafeTimedSerializer(current_app.config['SECRET_KEY']).dumps(email, salt='password-reset-salt')

            reset_url = url_for('auth.reset_password', token=token, _external=True)

            # Send email
            msg = Message(
                subject="Password Reset Request",
                recipients=[email],
                body=f"Hi {user.first_name},\n\nClick the link below to reset your password:\n{reset_url}\n\nIf you didn’t request this, please ignore this email."
            )
            print(msg)
            mail.send(msg)

            flash('Password reset link has been sent to your email.', 'success')
            return redirect(url_for('auth.signIn'))
        else:
            flash('Email not found. Please check and try again.', 'error')

    return render_template('forgot-password.html')

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = URLSafeTimedSerializer(current_app.config['SECRET_KEY']).loads(
            token, salt='password-reset-salt', max_age=3600  # valid for 30 min
        )
    except SignatureExpired:
        flash('The reset link has expired. Please request a new one.', 'error')
        return redirect(url_for('auth.forgot_password'))
    except BadSignature:
        flash('Invalid reset link.', 'error')
        return redirect(url_for('auth.forgot_password'))

    user = User.query.filter_by(email=email).first_or_404()

    if request.method == 'POST':
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(request.url)
        
        if new_password == user.password:
            flash("You can't use your old password again!")
            return render_template('reset-password.html')

        user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Your password has been reset successfully. Please log in.', 'success')
        return redirect(url_for('auth.signIn'))

    return render_template('reset-password.html', token=token)




@auth.route('/update-profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    """Display or update user profile"""
    user_profile = Profile.query.filter_by(user_id=current_user.id).first()

    # GET — render form
    if request.method == 'GET':
        return render_template('update-profile.html', profile=user_profile)

    # POST — handle form submission
    bio = request.form.get('bio', '').strip()
    lg_of_origin = request.form.get('LG_of_origin', '').strip()
    state_of_origin = request.form.get('state_of_origin', '').strip()
    country_of_origin = request.form.get('country_of_origin', '').strip()
    lg_of_residence = request.form.get('LG_of_residence', '').strip()
    state_of_residence = request.form.get('state_of_residence', '').strip()
    country_of_residence = request.form.get('country_of_residence', '').strip()
    address = request.form.get('address', '').strip()

    avatar_file = request.files.get('avatar_url')

    try:
        # Handle avatar upload
        avatar_filename = None
        if avatar_file and allowed_file(avatar_file.filename) and validate_file_size(avatar_file):
            filename = secure_filename(avatar_file.filename)
            avatar_path = os.path.join(UPLOAD_FOLDER, filename)
            avatar_file.save(avatar_path)
            avatar_filename = filename

        if user_profile:
            # Update existing profile
            user_profile.state_of_origin = state_of_origin or user_profile.state_of_origin
            user_profile.country_of_origin = country_of_origin or user_profile.country_of_origin
            user_profile.lg_of_origin = lg_of_origin or user_profile.lg_of_origin
            user_profile.state_of_residence = state_of_residence or user_profile.state_of_residence
            user_profile.country_of_residence = country_of_residence or user_profile.country_of_residence
            user_profile.lg_of_residence = lg_of_residence or user_profile.lg_of_residence
            user_profile.address = address or user_profile.address
            user_profile.bio = bio or user_profile.bio

            if avatar_filename:
                user_profile.avatar_url = avatar_filename

        else:
            # Create new profile
            new_profile = Profile(
                user_id=current_user.id,
                bio=bio or None,
                state_of_origin=state_of_origin or None,
                country_of_origin=country_of_origin or None,
                lg_of_origin=lg_of_origin or None,
                avatar_url=avatar_filename or None,
                state_of_residence=state_of_residence or None,
                country_of_residence=country_of_residence or None,
                lg_of_residence=lg_of_residence or None,
                address=address or None
            )
            db.session.add(new_profile)

        db.session.commit()
        flash('✅ Profile updated successfully!', 'success')

    except Exception as e:
        db.session.rollback()
        logging.error("Error updating profile: %s", e)
        flash(f'❌ An error occurred while updating your profile: {e}', 'error')

    return redirect(url_for('main.Profile'))



@auth.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    
    if not user:
        flash(f"User with ID {user_id} not found.", "error")
        return redirect(url_for('main.manage_user'))  # Redirect back to users list

    try:
        db.session.delete(user)
        db.session.commit()
        flash(f"User {user.first_name} has been deleted successfully.", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"An error occurred while deleting the user: {str(e)}", "error")

    return redirect(url_for('main.manage_user'))



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.signIn'))

