from marshmallow import (Schema, fields, validate)

class CreateBlackListSchema(Schema):
    ban_driver_id = fields.String(required=True)
    passenger_id = fields.String(required=True)
