from flask import Blueprint

mechanics_bp = Blueprint('mechanics_bp', __name__)

from . import routes  # Import routes after creating the blueprint to avoid circular imports