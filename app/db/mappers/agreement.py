from sqlalchemy.sql import select, exists

from app.db.models import Order as OrderModel
from app.order.domain.status import PassengerOrderStatus
from app.utils.mapper import Mapper


class AgreementMapper(Mapper):

    async def find_current(self, driver):
        async with self.engine.acquire() as conn:
            join = (
                self.model
                .join(
                    OrderModel,
                    OrderModel.c.id == self.model.c.order_id
                )
            )

            query = (
                select([self.model])
                .select_from(join)
                .where(
                    (self.model.c.id == driver.id)
                    & (
                        (OrderModel.c.status == PassengerOrderStatus.SEARCHING.value)
                        | (OrderModel.c.status == PassengerOrderStatus.IN_MID_COURSE.value)
                    )
                )
            )

            result = await conn.execute(query)
            data = await result.fetchone()

            if data is None:
                return None

            return self.entity_cls(**data)
