from flask import Flask
from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

load_dotenv()

cred = credentials.Certificate(os.environ.get("GOOGLE_AUTHORIZATION_CREDENTIALS"))
firebase_admin.initialize_app(cred)

db = firestore.client()

def create_app():
    app = Flask(__name__)

    # Register Blueprints here
    # from .routes import example_bp
    # app.register_blueprint(example_bp)
    return app
