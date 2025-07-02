from flask import Blueprint

customers_bp = Blueprint('customers_bp', __name__)

from . import routes  # Import routes after creating the blueprint to avoid circular imports