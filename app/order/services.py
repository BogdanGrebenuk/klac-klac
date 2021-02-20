from app.order import schemas
from app.order.domain.entity import Order


class OrderCreator:

    def __init__(self, validator):
        self.validator = validator

    async def create(self, create_order_dto):
        self.validator.validate(create_order_dto, schemas.CreateOrderSchema)

        order = Order(
            id=create_order_dto.id,
            from_=create_order_dto.from_,
            to=create_order_dto.to,
            passenger_id=create_order_dto.passenger_id,
            driver_id=None,
            status=create_order_dto.status
        )

        return order
