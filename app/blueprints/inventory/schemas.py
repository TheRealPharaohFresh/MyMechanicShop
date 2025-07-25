from app.models import Inventory
from app.extensions import ma
from marshmallow import Schema, fields



# Schema

class InventorySchema(ma.SQLAlchemyAutoSchema): 
    class Meta:
        model = Inventory
        load_instance = True
        include_relationships = True  # Include related fields
inventory_schema = InventorySchema()
inventory_schemas = InventorySchema(many=True)


class InventoryUsageSchema(Schema):
    inventory_id = fields.Int(required=True)
    quantity = fields.Int(required=True)

    class Meta:
        fields = ('inventory_id','quantity')

inventory_usage_schema = InventoryUsageSchema()
inventory_usage_schemas = InventoryUsageSchema(many=True)