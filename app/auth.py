from flask import Blueprint, render_template, redirect, url_for, request, flash,current_app
from flask_login import login_user, logout_user, login_required
import re
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.model import User
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

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'error')
    return redirect(url_for('main.index'))
