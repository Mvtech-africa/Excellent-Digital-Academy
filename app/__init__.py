from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

db = SQLAlchemy()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address)  # ✅ Create limiter here

def create_app():
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()
    
    # Config
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # For production with Redis
    app.config["RATELIMIT_STORAGE_URI"] = os.getenv("REDIS_URL", "redis://localhost:6379")
    # Init extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    limiter.init_app(app)  # ✅ Initialize with app
    login_manager.login_view = 'auth.signIn'  # ✅ Fixed
    
    # Import models AFTER db init
    with app.app_context():
        from . import model
        
        @login_manager.user_loader
        def load_user(user_id):
            return model.User.query.get(int(user_id))
    
    # Register blueprints
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)