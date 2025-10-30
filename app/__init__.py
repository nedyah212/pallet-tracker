import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_FLASK_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    bcrypt.init_app(app)

    from app.models import Shipment, Pallet, Trailer, OversizedGood

    with app.app_context():
        db.create_all()

    from app.blueprints import core_bp, settings_bp

    app.register_blueprint(core_bp)
    app.register_blueprint(settings_bp)

    return app
