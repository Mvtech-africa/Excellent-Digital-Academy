from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.model import User

auth = Blueprint('auth', __name__)

@auth.route('/signIn', methods=['GET', 'POST'])
def signIn():
    """if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and password is correct
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.profile'))
        else:
            flash('Invalid email or password. Please try again.')
            return redirect(url_for('auth.signIn'))"""
    
    return render_template('signin.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        
        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Email already exists. Please login.')
            return redirect(url_for('auth.signIn'))
        
        # Create new user with hashed password
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            phone=phone
        )
        
        # Add to database
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please login.')
        return redirect(url_for('auth.signIn'))
    
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))