from marshmallow import (Schema, fields, validate)


class CreateOrderSchema(Schema):
    id = fields.String(required=True)
    from_ = fields.String(required=True)
    to = fields.String(required=True)
    passenger_id = fields.String(required=True)
    status = fields.String(required=True)
    geolocation = fields.String(required=True)