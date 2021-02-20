from app.utils.transformer import Transformer


class AgreementTransformer(Transformer):

    async def transform(self, agreement):
        return {
            'id': agreement.id,
            'driverId': agreement.driver_id,
            'orderId': agreement.order_id
        }
