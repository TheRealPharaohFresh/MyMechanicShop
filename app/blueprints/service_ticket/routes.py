from .schemas import (
    service_ticket_schema, service_tickets_schema,
    update_service_ticket_inventory_schema
)
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Mechanic, Service_Ticket, Inventory, db, ServiceTicketInventory
from . import service_tickets_bp
from app.extensions import limiter
from app.utils.util import token_required


# Create a new service ticket (with mechanics and parts)
@service_tickets_bp.route("/", methods=["POST"])
def create_service_ticket():
    data = request.get_json()
    mechanic_ids = data.pop("mechanic_ids", [])
    parts = data.pop("parts", [])  # Expect list of {inventory_id, quantity}

    try:
        new_ticket = service_ticket_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Attach mechanics
    mechanics = db.session.query(Mechanic).filter(Mechanic.id.in_(mechanic_ids)).all()
    new_ticket.mechanics = mechanics

    # Add parts associations & deduct inventory
    for part in parts:
        inventory_id = part.get("inventory_id")
        quantity = part.get("quantity", 1)

        inventory_item = db.session.get(Inventory, inventory_id)
        if not inventory_item:
            return jsonify({"error": f"Inventory item {inventory_id} not found"}), 404

        if inventory_item.quantity < quantity:
            return jsonify({"error": f"Not enough stock for inventory item {inventory_item.name}"}), 400

        assoc = ServiceTicketInventory(
            service_ticket=new_ticket,
            inventory=inventory_item,
            quantity=quantity
        )
        new_ticket.inventory_associations.append(assoc)

        # Deduct from inventory stock
        inventory_item.quantity -= quantity

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


# Get service tickets for logged-in customer (token required)
@service_tickets_bp.route("/my-tickets", methods=["GET"])
@token_required
def get_my_service_tickets(customer_id):
    service_tickets = db.session.query(Service_Ticket).filter(Service_Ticket.customer_id == customer_id).all()
    if not service_tickets:
        return jsonify({"message": "No service tickets found for this customer"}), 404
    return service_tickets_schema.jsonify(service_tickets), 200


# Bulk update mechanics on a service ticket
@service_tickets_bp.route("/<int:ticket_id>/mechanics", methods=["PUT"])
@limiter.limit("3 per day")
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


# Update inventory parts on a service ticket with stock adjustments
@service_tickets_bp.route("/<int:ticket_id>/inventory", methods=["PUT"])
@limiter.limit("3 per day")
def update_service_ticket_inventory(ticket_id):
    service_ticket = db.session.get(Service_Ticket, ticket_id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    try:
        update_data = update_service_ticket_inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Add parts
    for part in update_data.get("add_parts", []):
        inventory_id = part["inventory_id"]
        add_quantity = part.get("quantity", 1)

        inventory_item = db.session.get(Inventory, inventory_id)
        if not inventory_item:
            return jsonify({"error": f"Inventory item {inventory_id} not found"}), 404

        if inventory_item.quantity < add_quantity:
            return jsonify({"error": f"Not enough stock for inventory item {inventory_item.name}"}), 400

        assoc = next((a for a in service_ticket.inventory_associations if a.inventory_id == inventory_id), None)
        if assoc:
            assoc.quantity += add_quantity
        else:
            assoc = ServiceTicketInventory(
                service_ticket_id=service_ticket.id,
                inventory_id=inventory_id,
                quantity=add_quantity
            )
            service_ticket.inventory_associations.append(assoc)

        inventory_item.quantity -= add_quantity

    # Remove parts
    for part in update_data.get("remove_parts", []):
        inventory_id = part["inventory_id"]
        remove_quantity = part.get("quantity", 1)

        assoc = next((a for a in service_ticket.inventory_associations if a.inventory_id == inventory_id), None)
        if not assoc:
            return jsonify({"error": f"Inventory item {inventory_id} not associated with this ticket"}), 404

        if remove_quantity >= assoc.quantity:
            inventory_item = db.session.get(Inventory, inventory_id)
            inventory_item.quantity += assoc.quantity
            service_ticket.inventory_associations.remove(assoc)
            db.session.delete(assoc)
        else:
            assoc.quantity -= remove_quantity
            inventory_item = db.session.get(Inventory, inventory_id)
            inventory_item.quantity += remove_quantity

    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200


# Delete a specific service ticket (refund inventory stock)
@service_tickets_bp.route("/<int:ticket_id>", methods=["DELETE"])
@limiter.limit("5 per day")
def delete_service_ticket(ticket_id):
    service_ticket = db.session.get(Service_Ticket, ticket_id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    # Refund inventory stock
    for assoc in service_ticket.inventory_associations:
        assoc.inventory.quantity += assoc.quantity

    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({"message": "Service ticket deleted successfully"}), 204


# Remove a specific mechanic from a ticket
@service_tickets_bp.route("/<int:ticket_id>/mechanics/<int:mechanic_id>", methods=["DELETE"])
@limiter.limit("3 per day")
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


# Get all mechanics assigned to a ticket
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

