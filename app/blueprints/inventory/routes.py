from .schemas import inventory_schema, inventory_schemas, inventory_usage_schema
from flask import  request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Service_Ticket,Inventory, db
from . import inventory_bp
from app.extensions import limiter, cache
from app.utils.util import  token_required


@inventory_bp.route("/", methods=["POST"])
def create_inventory():
    try:
        new_inventory = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    existing_inventory = db.session.scalar(
        select(Inventory).where(Inventory.name == new_inventory.name)
    )
    if existing_inventory:
        return jsonify({"error": "Inventory item already exists"}), 400

    db.session.add(new_inventory)
    db.session.commit()
    return inventory_schema.jsonify(new_inventory), 201

@inventory_bp.route("/", methods=["GET"])
@cache.cached(timeout=90)  # Cache for 90 seconds
def get_inventories():
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        query = select(Inventory)
        inventories = db.paginate(query, page=page, per_page=per_page).items
        return inventory_schemas.jsonify(inventories), 200
    except Exception as e:
        query = select(Inventory)
        inventories = db.session.execute(query).scalars().all()
    return inventory_schemas.jsonify(inventories), 200

@inventory_bp.route("/<int:inventory_id>", methods=["GET"])
def get_inventory(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)
    if not inventory:
        return jsonify({"error": "Inventory item not found"}), 404
    return inventory_schema.jsonify(inventory), 200

@inventory_bp.route("/<int:inventory_id>", methods=["PUT"])
def update_inventory(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)
    if not inventory:
        return jsonify({"error": "Inventory item not found"}), 404

    try:
        updated_inventory = inventory_schema.load(request.json, instance=inventory, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.commit()
    return inventory_schema.jsonify(updated_inventory), 200


@inventory_bp.route("/<int:inventory_id>", methods=["DELETE"])
def delete_inventory(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)
    if not inventory:
        return jsonify({"error": "Inventory item not found"}), 404

    db.session.delete(inventory)
    db.session.commit()
    return jsonify({"message": "Inventory item deleted successfully"}), 204