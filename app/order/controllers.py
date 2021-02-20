import asyncio
import uuid

from aiohttp import web

from app.order.domain.status import PassengerOrderStatus, DriverOrderStatus
from app.order.dto import CreateOrderDto


# POST /api/orders
async def create_order(
        request,
        passenger_mapper,
        order_creator,
        order_mapper,
        order_transformer,
        order_timeout_checker
        ):
    user_id = request.get('user_id')
    body = await request.post()
    passenger = await passenger_mapper.get_one_by(user_id=user_id)

    order = await order_creator.create(
        CreateOrderDto(
            id=str(uuid.uuid4()),
            passenger_id=passenger.id,
            from_=body.get('from'),
            to=body.get('to'),
            status=PassengerOrderStatus.SEARCHING.value
        ),
        body.get('image'),
        request.app.public_dir
    )

    await order_mapper.create(order)
    asyncio.create_task(order_timeout_checker.launch(order.id))

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
    orders = await order_mapper.find_by(status=PassengerOrderStatus.SEARCHING.value)
    return web.json_response({
        'orders': await order_transformer.transform_many(orders)
    })


# GET /api/orders/{order_id}
async def get_order_status(
        request,
        driver_mapper,
        passenger_mapper,
        order_mapper,
        agreement_mapper
        ):
    order = await order_mapper.get_one_by(request.match_info.get('order_id'))

    user_id = request.get('user_id')
    driver = await driver_mapper.find_one_by(user_id=user_id)
    if driver is not None:
        return await get_order_status_for_driver(
            order,
            driver,
            agreement_mapper
        )

    passenger = await passenger_mapper.find_one_by(user=user_id)
    if passenger is not None:
        return await get_order_status_for_passenger(
            order,
            passenger
        )

    return web.json_response({
        'error': 'How did you get there?',
        'payload': {}
    }, status=400)


async def get_order_status_for_passenger(
        order,
        passenger
        ):
    if order.passenger_id != passenger.id:
        return web.json_response({
            'error': 'This is not your order!',
            'payload': {}
        }, status=403)

    return web.json_response({
        'status': order.status
    })


async def get_order_status_for_driver(
        order,
        driver,
        agreement_mapper
        ):
    related_agreements = await agreement_mapper.find_by(
        order_id=order.id,
        driver_id=driver.id
    )

    if len(related_agreements) == 0:
        return web.json_response({
            'error': 'Driver has not posted any agreement yet to this order',
            'payload': {}
        }, status=400)

    if order.driver_id is None:
        return web.json_response({
            'status': DriverOrderStatus.PENDING.value
        })

    if order.driver_id != driver.id:
        return web.json_response({
            'status': DriverOrderStatus.REJECTED.value
        })

    return web.json_response({
        'status': DriverOrderStatus.ACCEPTED.value
    })