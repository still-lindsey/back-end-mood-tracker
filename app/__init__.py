from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    # Import models here for Alembic setup
    # from app.models.ExampleModel import ExampleModel
    
    from .models.day import Day
    from .models.entry import Entry
    from .models.month import Month

    
    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import days_bp
    app.register_blueprint(days_bp)

    from .routes import quotes_bp
    app.register_blueprint(quotes_bp)

    from .routes import months_bp
    app.register_blueprint(months_bp)

    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    return app
