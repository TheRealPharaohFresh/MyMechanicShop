from flask import Blueprint

inventory_bp = Blueprint('inventory_bp', __name__)

from . import routes  # Import routes after creating the blueprint to avoid circular imports