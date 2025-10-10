# create_superuser.py
from app import create_app, db
from app.model import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter admin email: ")
    phone = input("Enter phone number: ")
    password = input("Enter admin password: ")
    confirm_password = input("Confirm password: ")

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        print("❌ A user with that email already exists.")
    elif password != confirm_password:
        print("❌ Passwords do not match. Please try again.")
    else:
        hashed_pw = generate_password_hash(password)
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=hashed_pw,
            tos=True,
            is_admin=True
        )
        db.session.add(user)
        db.session.commit()
        print("✅ Superuser created successfully!")
