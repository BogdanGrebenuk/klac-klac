from marshmallow import (Schema, fields, validate)

class CreateWhiteListSchema(Schema):
    driver_id = fields.String(required=True)
    passenger_id = fields.String(required=True)
