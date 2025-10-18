import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

load_dotenv()
db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv('SECRET_FLASK_KEY')
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    bcrypt.init_app(app)

    from .routes import main

    app.register_blueprint(main)

    return app