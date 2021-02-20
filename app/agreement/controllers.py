# POST /api/agreement - only for drivers
import uuid

from aiohttp import web

from app.agreement.dto import CreateAgreementDto


# POST /api/agreements - only for drivers
async def create_agreement(
        request,
        driver_mapper,
        agreement_creator,
        agreement_mapper,
        order_mapper,
        agreement_transformer
        ):
    body = await request.json()
    user_id = request.get('user_id')
    # to ensure driver exists
    driver = await driver_mapper.get_one_by(user_id=user_id)
    order = await order_mapper.get_one_by(id=body.get('order_id'))

    agreement = await agreement_creator.create_agreement(
        CreateAgreementDto(
            id=str(uuid.uuid4()),
            driver_id=driver.id,
            order_id=order.id
        )
    )

    await agreement_mapper.create(agreement)

    return web.json_response({
        'agreement': await agreement_transformer.transform(agreement)
    })


# GET /api/orders/{order_id}/agreements - only for passengers
async def get_agreements(
        request,
        passenger_mapper,
        agreement_mapper,
        agreement_transformer
        ):
    user_id = request.get('user_id')
    # to ensure driver exists
    passenger = await passenger_mapper.get_one_by(user_id=user_id)

    order_id = request.match_info.get('order_id')

    agreements = await agreement_mapper.find_by(order_id=order_id)

    return web.json_response({
        'agreements': await agreement_transformer.transform_many(agreements)
    })


# POST /api/agreements/{agreement_id}/select
async def select_agreement(
        request,
        passenger_mapper,
        agreement_mapper,
        order_mapper,
        agreement_transformer
        ):
    user_id = request.get('user_id')
    # to ensure driver exists
    passenger = await passenger_mapper.get_one_by(user_id=user_id)

    agreement_id = request.match_info.get('agreement_id')
    agreement = await agreement_mapper.get_one_by(id=agreement_id)
    order = await order_mapper.get_one_by(id=agreement.order_id)

    order.driver_id = agreement.driver_id

    await order_mapper.update(order)

    return web.json_response({
        'agreement': await agreement_transformer.transform(agreement)
    })
