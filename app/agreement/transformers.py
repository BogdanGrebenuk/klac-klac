from app.utils.transformer import Transformer


class AgreementTransformer(Transformer):

    def __init__(self, user_mapper):
        self.user_mapper = user_mapper

    async def transform(self, agreement):
        user = await self.user_mapper.find_one_by(id=agreement.driver_id)
        return {
            'id': agreement.id,
            'driverId': agreement.driver_id,
            'driver': {
                "id": user.id,
                "firstName": user.first_name,
                "lastName": user.last_name,
            },
            'orderId': agreement.order_id
        }
