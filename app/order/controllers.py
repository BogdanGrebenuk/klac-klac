import asyncio
import uuid

from aiohttp import web

from app.order.domain.status import PassengerOrderStatus, DriverOrderStatus
from app.order.dto import CreateOrderDto


# POST /api/orders
from app.utils.mapper import EntityNotFound


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
        passenger_mapper,
        order_mapper,
        order_transformer
        ):
    user_id = request.get('user_id')

    driver = await driver_mapper.find_one_by(user_id=user_id)
    if driver is not None:
        return await get_orders_for_driver(driver, order_mapper, order_transformer)

    passenger = await passenger_mapper.find_one_by(user_id=user_id)
    if passenger is not None:
        return await get_orders_for_passenger(passenger, order_mapper, order_transformer)

    raise EntityNotFound('There is no user with such id')


async def get_orders_for_driver(driver, order_mapper, order_transformer):
    orders = await order_mapper.find_pending_orders_for_driver(driver)
    return web.json_response({
        'orders': await order_transformer.transform_many(orders)
    })


async def get_orders_for_passenger(passenger, order_mapper, order_transformer):
    orders = await order_mapper.find_by(
        passenger_id=passenger.id
    )
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

    raise EntityNotFound('There is no user with such id')


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


# POST /api/orders/{order_id}/move_status
async def update_order_status(
        request,
        order_mapper,
        driver_mapper,
        order_transformer
        ):
    order = await order_mapper.get_one_by(request.match_info.get('order_id'))
    driver = await driver_mapper.get_one_by(user_id=request.get('user_id'))

    if order.driver_id != driver.id:
        return web.json_response({
            'error': 'This is not your order!',
            'payload': {}
        }, status=400)

    if order.status not in PassengerOrderStatus.get_manually_updatable_statuses():
        return web.json_response({
            'error': 'The order in the current status is not updatable',
            'payload': {
                'currentStatus': order.status
            }
        }, status=400)

    await move_to_the_next_status(order)

    await order_mapper.update(order)

    return web.json_response({
        'order': await order_transformer.transform(order)
    })


async def move_to_the_next_status(order):
    current_status = order.status

    if current_status == PassengerOrderStatus.IN_MID_COURSE.value:
        order.status = PassengerOrderStatus.IN_PROGRESS.value
        return

    if current_status == PassengerOrderStatus.IN_PROGRESS.value:
        order.status = PassengerOrderStatus.COMPLETED.value
        return

    raise web.HTTPBadRequest(text="You shouldn't be here")
