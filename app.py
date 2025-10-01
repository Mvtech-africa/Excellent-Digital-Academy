from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import  Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
import secrets


app = Flask(__name__)
#configure the SQLite database relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# set secret key
app.config["SECRET_KEY"] = secrets.token_hex(16)
#initialize the database        
db = SQLAlchemy(app)


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement="auto")
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.id!r})"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def users():
    try:
        users = db.session.execute(db.select(User).order_by(User.id)).scalars()
        return render_template("user.html", users=users)
    except Exception as e:
        flash("Signup failed: " + str(e), "error")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone")

        if not (first_name and last_name and email and password and phone):
            flash("All fields are required.", "error")
            return render_template('signup.html')

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please log in.", "warning")
            return redirect(url_for("signIn"))

        try:
            hashed_pw = generate_password_hash(password)
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=hashed_pw,
                phone=phone
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Signup successful! Please log in.", "success")
            return redirect(url_for("signIn"))
        except Exception as e:
            db.session.rollback()
            flash("Signup failed: " + str(e), "error")

    return render_template('signup.html')


# --- SIGNIN ---
@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user'] = user.email
            flash("Login successful!", "success")
            return redirect(url_for('index'))  # replace with your dashboard
        else:
            flash("Invalid email or password", "danger")

    return render_template('signin.html')

if __name__ == '__main__':
    app.run(debug=True)