from flask import Blueprint

service_tickets_bp = Blueprint('service_tickets_bp', __name__)

from . import routes  # Import routes after creating the blueprint to avoid circular imports