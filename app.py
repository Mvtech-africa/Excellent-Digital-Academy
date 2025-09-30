from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import  Integer, String
from sqlalchemy.orm import Mapped, mapped_column



app = Flask(__name__)
#configure the SQLite database relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#initialize the database        
db = SQLAlchemy(app)


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)

    def __repr__(self) -> str:
        return f"User(id={self.id!r})"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def users():
    users = db.session.execute(db.select(User).order_by(User.id)).scalars()
    return render_template("user.html", users=users)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone")
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=password, phone=phone)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("users"))   
    return render_template('signup.html')

@app.route('/signIn')
def signIn():
    return render_template('signin.html')


if __name__ == '__main__':
    app.run(debug=True)