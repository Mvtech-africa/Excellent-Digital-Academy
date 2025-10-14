# create_superuser.py
from app import create_app, db
from app.model import User, Role  # ✅ import Role Enum
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    print("🧑‍💻 Create Superuser")
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
        hashed_pw = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=hashed_pw,
            tos=True,
            role=Role.ADMIN   # ✅ set role instead of Role=True
        )
        db.session.add(user)
        db.session.commit()
        print(f"✅ Superuser '{email}' created successfully with ADMIN privileges!")
