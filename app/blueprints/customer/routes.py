from .schemas import customer_schema, customers_schema, login_schema
from flask import  request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Customer, db
from . import customers_bp
from app.extensions import limiter, cache
from app.utils.util import encode_token, token_required




# Routes

@customers_bp.route("/login", methods=["POST"])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials["email"]
        password = credentials["password"]
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalars().first()

    if customer and customer.password == password:
        token = encode_token(customer.id)

        response = {
            "status": "success",
            "message": "Welcome Inside The Egyptian Pyramids",
            "token": token,
        }

        return jsonify(response), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

    


#Create a new customer
@customers_bp.route("/", methods=["POST"])
@limiter.limit("5 per day")  # Limit to 5 requests per minute
def create_customer():
    try:
        new_customer = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    existing_customer = db.session.scalar(
        select(Customer).where(Customer.email == new_customer.email)
    )
    if existing_customer:
        return jsonify({"error": "Customer already exists"}), 400
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

# Get all customers
@customers_bp.route("/", methods=["GET"])
@cache.cached(timeout=20)  # Cache the response for 60 seconds
def get_customers():
    customers = db.session.execute(select(Customer)).scalars().all()
    return customers_schema.jsonify(customers), 200


# Get a customer by ID
@customers_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return customer_schema.jsonify(customer), 200

# update a specific customer
@customers_bp.route("/<int:customer_id>", methods=["PUT"])
@limiter.limit("5 per month")  # Limit to 5 requests per minute
@token_required
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    print("request.json:", request.json)  # This line prints the JSON

    try:
        updated_customer = customer_schema.load(request.json, instance=customer, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.commit()
    return customer_schema.jsonify(updated_customer), 200

# Delete a specific customer
@customers_bp.route("/", methods=["DELETE"])
@token_required
@limiter.limit("5 per day")  # Limit to 5 requests per minute
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f'Customer id: {customer_id} Was Deleted Successfully'}), 204

