from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Inventory, db
from . import inventory_bp
from app.extensions import limiter, cache
from .schemas import inventory_schema, inventory_schemas, inventory_usage_schema

# Create a new inventory item
@inventory_bp.route("/", methods=["POST"])
def create_inventory():
    try:
        new_inventory = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.add(new_inventory)
    db.session.commit()
    return inventory_schema.jsonify(new_inventory), 201

# Get all inventory items
@inventory_bp.route("/", methods=["GET"])
@limiter.limit("10 per minute")
@cache.cached(timeout=60)
def get_inventory():
    inventory = db.session.scalars(select(Inventory)).all()
    return inventory_schemas.jsonify(inventory), 200

# Get a specific inventory item
@inventory_bp.route("/<int:inventory_id>", methods=["GET"])
def get_inventory_by_id(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)
    if not inventory:
        return jsonify({"error": "Inventory item not found"}), 404
    return inventory_schema.jsonify(inventory), 200

# Update inventory item
@inventory_bp.route("/<int:inventory_id>", methods=["PUT"])
def update_inventory( inventory_id):
    inventory = db.session.get(Inventory, inventory_id)
    if not inventory:
        return jsonify({"error": "Inventory item not found"}), 404

    try:
        updated_data = inventory_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in updated_data.items():
        setattr(inventory, key, value)

    db.session.commit()
    return inventory_schema.jsonify(inventory), 200

# Delete inventory item
@inventory_bp.route("/<int:inventory_id>", methods=["DELETE"])
def delete_inventory(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)
    if not inventory:
        return jsonify({"error": "Inventory item not found"}), 404

    db.session.delete(inventory)
    db.session.commit()
    return jsonify({"message": "Inventory item deleted"}), 200

#  Add usage to inventory (should be linked to service_ticket ideally)
@inventory_bp.route("/<int:inventory_id>/usage", methods=["POST"])
def add_inventory_usage(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)
    if not inventory:
        return jsonify({"error": "Inventory item not found"}), 404

    try:
        usage_data = inventory_usage_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    quantity_used = usage_data["quantity"]
    if inventory.quantity < quantity_used:
        return jsonify({"error": "Insufficient inventory"}), 400

    inventory.quantity -= quantity_used
    db.session.commit()
    return jsonify({"message": f"{quantity_used} items deducted from inventory"}), 200

