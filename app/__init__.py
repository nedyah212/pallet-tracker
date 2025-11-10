import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
#from dotenv import load_dotenv

#load_dotenv()
db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "I forgot my env file at home today hahaha"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

    # Turn off in production
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["DEBUG"] = True

    db.init_app(app)
    bcrypt.init_app(app)

    from app.models import Shipment, Pallet, Trailer, OversizedGood

    with app.app_context():
        db.create_all()

    from app.blueprints import core_bp, settings_bp

    app.register_blueprint(core_bp)
    app.register_blueprint(settings_bp)

    return app
