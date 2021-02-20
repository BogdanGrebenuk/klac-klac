import uuid

from aiohttp import web

from app.order.dto import CreateOrderDto


# POST /api/orders
async def create_order(
        request,
        passenger_mapper,
        order_creator,
        order_mapper,
        order_transformer
        ):
    user_id = request.get('user_id')
    body = await request.post()
    passenger = await passenger_mapper.get_one_by(user_id=user_id)
    print(body)

    order = await order_creator.create(
        CreateOrderDto(
            id=str(uuid.uuid4()),
            passenger_id=passenger.id,
            from_=body.get('from'),
            to=body.get('to'),
            status='test'
        ),
        body.get('image'),
        request.app.public_dir
    )

    await order_mapper.create(order)

    return web.json_response({
        'order': await order_transformer.transform(order)
    })


# GET /api/orders - only for driver
async def get_orders(
        request,
        driver_mapper,
        order_mapper,
        order_transformer
        ):
    user_id = request.get('user_id')
    # to ensure driver exists
    driver = await driver_mapper.get_one_by(user_id=user_id)
    orders = await order_mapper.find_all()
    return web.json_response({
        'orders': await order_transformer.transform_many(orders)
    })
