from app.utils.transformer import Transformer


class OrderTransformer(Transformer):

    async def transform(self, order):
        return {
            'id': order.id,
            'from': order.from_,
            'to': order.to,
            'passengerId': order.passenger_id,
            'driverId': order.driver_id,
            'status': order.status,
            'image': order.image
        }
