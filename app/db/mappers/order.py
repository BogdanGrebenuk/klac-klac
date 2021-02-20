from sqlalchemy.sql import select, exists

from app.db.models import User as UserModel, BlackList as BlackListModel
from app.order.domain.status import PassengerOrderStatus
from app.utils.mapper import Mapper


class OrderMapper(Mapper):

    async def find_pending_orders_for_driver(self, driver):
        async with self.engine.acquire() as conn:
            join = (
                self.model
                .join(
                    UserModel,
                    UserModel.c.id == self.model.c.passenger_id
                )
            )

            query = (
                select([self.model])
                .select_from(join)
                .where(
                    (self.model.c.status == PassengerOrderStatus.SEARCHING.value)
                    & (
                        ~exists(
                            select([BlackListModel])
                            .where(
                                (BlackListModel.c.passenger_id == self.model.passenger_id)
                                & (BlackListModel.c.ban_driver_id == driver.id)
                            )
                        )
                    )
                )
            )

            result = await conn.execut(query)
            data = await result.fetchall()

            return [self.entity_cls(**i) for i in data]

