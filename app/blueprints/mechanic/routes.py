from .schemas import mechanic_schema, mechanics_schema
from flask import  request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Mechanic, db
from . import mechanics_bp




# Create a new mechanic
@mechanics_bp.route("/", methods=["POST"])
def create_mechanic():
    try:
        new_mechanic = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    existing_mechanic = db.session.scalar(
        select(Mechanic).where(Mechanic.email == new_mechanic.email)
    )
    if existing_mechanic:
        return jsonify({"error": "Mechanic already exists"}), 400

    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201


# Get all mechanics 
@mechanics_bp.route("/", methods=["GET"])
# @cache.cached(timeout=60)  # Cache for 60 seconds
def get_mechanics():
    try:
        page = int(request.args.get("page"))
        per_page = int(request.args.get("per_page"))
        query = select(Mechanic)
        mechanics = db.paginate(query, page=page, per_page=per_page).items
        return mechanics_schema.jsonify(mechanics), 200
    except Exception as e:  # Catch specific exceptions if possible
        query = select(Mechanic)
        mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics), 200



# Get a mechanic by ID
@mechanics_bp.route("/<int:mechanic_id>", methods=["GET"])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    return mechanic_schema.jsonify(mechanic), 200


# Update a specific mechanic
@mechanics_bp.route("/<int:mechanic_id>", methods=["PUT"])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    try:
        updated_mechanic = mechanic_schema.load(
            request.json, instance=mechanic, partial=True
        )
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.commit()
    return mechanic_schema.jsonify(updated_mechanic), 200


# Delete a specific mechanic
@mechanics_bp.route("/<int:mechanic_id>", methods=["DELETE"])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": "Mechanic deleted successfully"}), 204

#most popular mechanics
@mechanics_bp.route("/popular", methods=["GET"])
def get_popular_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()

    mechanics.sort(key=lambda m: len(m.service_tickets), reverse=True)
    
    return mechanics_schema.jsonify(mechanics[:5]), 200  # Return top 5 mechanics by ticket count



@mechanics_bp.route("/search", methods=["GET"])
def search_mechanics():
    name = request.args.get("name")

    query = select(Mechanic).where(Mechanic.name.like(f"%{name}%")) if name else select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()


    return (
    (mechanics_schema.jsonify(mechanics), 200)
    if mechanics
    else (jsonify({"message": "No mechanics found"}), 404)
)

