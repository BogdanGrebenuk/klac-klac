import uuid

from app.order import schemas
from app.order.domain.entity import Order


class OrderCreator:

    def __init__(self, validator):
        self.validator = validator

    async def create(self, create_order_dto, image, path):
        self.validator.validate(create_order_dto, schemas.CreateOrderSchema)

        file_name = f"{uuid.uuid4()}{image.filename}"
        save_file_field_image(image.file, path + '/' + file_name)

        order = Order(
            id=create_order_dto.id,
            from_=create_order_dto.from_,
            to=create_order_dto.to,
            passenger_id=create_order_dto.passenger_id,
            driver_id=None,
            status=create_order_dto.status,
            image=file_name
        )

        return order

def save_file_field_image(source, path):
    with open(path, "wb") as file:
        file.write(source.read())
