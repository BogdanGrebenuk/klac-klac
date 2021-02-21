import uuid

import asyncio

from app.order import schemas
from app.order.domain.entity import Order
from app.order.domain.status import PassengerOrderStatus


class OrderCreator:

    def __init__(self, validator):
        self.validator = validator

    async def create(self, create_order_dto, image, path):
        self.validator.validate(create_order_dto, schemas.CreateOrderSchema)

        file_name = None
        if image is not None:
            file_name = f"{uuid.uuid4()}{image.filename}"
            save_file_field_image(image.file, path + '/' + file_name)

        order = Order(
            id=create_order_dto.id,
            from_=create_order_dto.from_,
            to=create_order_dto.to,
            passenger_id=create_order_dto.passenger_id,
            driver_id=None,
            status=create_order_dto.status,
            image=file_name,
            geolocation=None
        )

        return order

def save_file_field_image(source, path):
    with open(path, "wb") as file:
        file.write(source.read())


class OrderTimeoutChecker:

    def __init__(self, order_mapper, agreement_mapper, logger):
        self.order_mapper = order_mapper
        self.agreement_mapper = agreement_mapper
        self.logger = logger

    async def launch(self, order_id, timeout=30):
        self.logger.info(f"[{order_id}] sleep {timeout} seconds")
        await asyncio.sleep(timeout)
        self.logger.info(f"[{order_id}] start to check order")
        order = await self.order_mapper.find(order_id)
        if order is None:
            self.logger.info(f"[{order_id}] order not found")
            return

        agreements = await self.agreement_mapper.find_by(order_id=order_id)
        if len(agreements) == 0:
            self.logger.info(f"[{order_id} nobody created agreement, start check again]")
            asyncio.create_task(self.launch(order_id))
            return

        # there are some agreements

        if order.driver_id is not None:  # user selects some agreement
            self.logger.info(f"[{order_id}] user select agreement")
            return

        self.logger.info(f"[{order_id}] select the first driver from agreement")
        order.driver_id = agreements[0].driver_id
        order.status = PassengerOrderStatus.IN_MID_COURSE.value

        await self.order_mapper.update(order)
