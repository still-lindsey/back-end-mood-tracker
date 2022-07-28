from flask import Blueprint, request, jsonify, make_response
from app import db

# example_bp = Blueprint('example_bp', __name__)
entries_bp = Blueprint('entries_bp', __name__, url_prefix="/entries")
