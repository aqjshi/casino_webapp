from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'main.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    login.init_app(app)
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    # IMPORTANT: Register the blueprint from errors.py using its bp attribute
    from app.main import errors as errors_module
    app.register_blueprint(errors_module.bp)
    
    return app

