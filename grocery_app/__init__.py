from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from grocery_app.extensions import db
import os

bcrypt = Bcrypt()
login_manager = LoginManager()
# Set the login view to the auth blueprint's login route
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    
    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev_key_for_now'
    
    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    # Import and register blueprints
    from grocery_app.routes import main
    app.register_blueprint(main)
    
    # Import and register auth blueprint
    from grocery_app.routes import auth
    app.register_blueprint(auth)
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    return app

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from grocery_app.models import User
    return User.query.get(int(user_id))