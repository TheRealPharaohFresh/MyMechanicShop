from marshmallow import fields
from app.extensions import ma
from app.models import  Service_Ticket
from app.blueprints.mechanic.schemas import MechanicSchema


# Schema



class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_Ticket
        load_instance = True
        include_fk = True  # to accept customer_id

    # Accept mechanic IDs on input
    mechanic_ids = fields.List(fields.Integer(), load_only=True)

    # Return full mechanic info in response
    mechanics = fields.Nested(MechanicSchema, many=True, dump_only=True)

class UpdateServiceTicketSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Integer(), load_only=True, required=True)
    remove_mechanic_ids = fields.List(fields.Integer(), load_only=True, required=True)
    class Meta:
        fields = ('add_mechanic_ids', 'remove_mechanic_ids')

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
update_service_ticket_schema = UpdateServiceTicketSchema()




