from marshmallow import fields, Schema
from app.extensions import ma
from app.models import Service_Ticket
from app.blueprints.mechanic.schemas import MechanicSchema
from app.blueprints.inventory.schemas import InventorySchema, InventoryUsageSchema

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_Ticket
        load_instance = True
        include_fk = True  # allows customer_id in input

    # Input: mechanic IDs
    mechanic_ids = fields.List(fields.Integer(), load_only=True)

    # Output: full mechanic data
    mechanics = fields.Nested(MechanicSchema, many=True, dump_only=True)

    inventory_parts = fields.Nested(InventorySchema, many=True)

    inventory_usage = fields.List(fields.Nested(InventoryUsageSchema))


class UpdateServiceTicketSchema(Schema):
    add_mechanic_ids = fields.List(fields.Integer(), load_only=True, required=True)
    remove_mechanic_ids = fields.List(fields.Integer(), load_only=True, required=True)

    class Meta:
        fields = ('add_mechanic_ids', 'remove_mechanic_ids')


class UpdateServiceTicketInventorySchema(Schema):
    add_parts = fields.List(
        fields.Nested(InventoryUsageSchema),
        required=True,
        load_only=True,
        metadata={
            "description": "List of parts to add. Example: [{'inventory_id': 1, 'quantity': 3}]"
        },
    )
    remove_parts = fields.List(
        fields.Integer(),
        required=True,
        load_only=True,
        metadata={
            "description": "List of inventory IDs to remove from ticket."
        },
    )

    class Meta:
        fields = ("add_parts", "remove_parts")


# Schema instances
service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
update_service_ticket_schema = UpdateServiceTicketSchema()
update_service_ticket_inventory_schema = UpdateServiceTicketInventorySchema()



