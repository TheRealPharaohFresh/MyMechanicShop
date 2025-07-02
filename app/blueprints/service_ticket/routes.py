from .schemas import service_ticket_schema, service_tickets_schema, update_service_ticket_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Mechanic, Service_Ticket, db
from . import service_tickets_bp
from app.extensions import limiter


# Create a new service ticket
@service_tickets_bp.route("/", methods=["POST"])
def create_service_ticket():
    data = request.get_json()
    mechanic_ids = data.pop("mechanic_ids", [])

    try:
        new_ticket = service_ticket_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Get full mechanic objects
    mechanics = db.session.query(Mechanic).filter(Mechanic.id.in_(mechanic_ids)).all()
    new_ticket.mechanics = mechanics

    db.session.add(new_ticket)
    db.session.commit()

    return service_ticket_schema.jsonify(new_ticket), 201


# Get all service tickets   
@service_tickets_bp.route("/", methods=["GET"])
def get_service_tickets():
    service_tickets = db.session.execute(select(Service_Ticket)).scalars().all()
    return service_tickets_schema.jsonify(service_tickets), 200


# Get a service ticket by ID
@service_tickets_bp.route("/<int:ticket_id>", methods=["GET"])
def get_service_ticket(ticket_id):
    service_ticket = db.session.get(Service_Ticket, ticket_id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    return service_ticket_schema.jsonify(service_ticket), 200


# Update a specific service ticket
@service_tickets_bp.route("/<int:ticket_id>", methods=["PUT"])
def update_service_ticket(ticket_id):
    try:
        ticket_updates = update_service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Service_Ticket).where(Service_Ticket.id == ticket_id)
    service_ticket = db.session.execute(query).scalars().first()

    for mechanic_id in ticket_updates["add_mechanic_ids"]:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic not in service_ticket:
            service_ticket.mechanics.append(mechanic)
    
    for mechanic_id in ticket_updates["add_mechanic_ids"]:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic not in service_ticket:
            service_ticket.mechanics.remove(mechanic)

    db.session.commit()
    return update_service_ticket_schema.jsonify(service_ticket), 200



#Update Mechanics on a Service Ticket

@service_tickets_bp.route("/<int:ticket_id>/mechanics", methods=["PUT"])
@limiter.limit("3 per day")  # Limit to 5 requests per minute
def update_service_ticket_mechanics(ticket_id):
    service_ticket = db.session.get(Service_Ticket, ticket_id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    mechanic_ids = request.json.get("mechanic_ids", [])
    if not isinstance(mechanic_ids, list):
        return jsonify({"error": "mechanic_ids must be a list"}), 400

    mechanics = db.session.query(Mechanic).filter(Mechanic.id.in_(mechanic_ids)).all()
    service_ticket.mechanics = mechanics

    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200

# Delete a specific service ticket
@service_tickets_bp.route("/<int:ticket_id>", methods=["DELETE"])
@limiter.limit("5 per day")  # Limit to 5 requests per minute
def delete_service_ticket(ticket_id):
    service_ticket = db.session.get(Service_Ticket, ticket_id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({"message": "Service ticket deleted successfully"}), 204

#Remove a Specific Mechanic from a Ticket

@service_tickets_bp.route("/<int:ticket_id>/mechanics/<int:mechanic_id>", methods=["DELETE"])
@limiter.limit("3 per day")  # Limit to 5 requests per minute
def remove_mechanic_from_service_ticket(ticket_id, mechanic_id):
    service_ticket = db.session.get(Service_Ticket, ticket_id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    if mechanic in service_ticket.mechanics:
        service_ticket.mechanics.remove(mechanic)
        db.session.commit()
        return jsonify({"message": "Mechanic removed from service ticket"}), 200
    else:
        return jsonify({"error": "Mechanic not assigned to this ticket"}), 400

#Get All Mechanics for a Ticket
@service_tickets_bp.route("/<int:ticket_id>/mechanics", methods=["GET"])
def get_mechanics_for_ticket(ticket_id):
    service_ticket = db.session.get(Service_Ticket, ticket_id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    return jsonify([
        {
            "id": mech.id,
            "name": mech.name,
            "email": mech.email
        } for mech in service_ticket.mechanics
    ])
