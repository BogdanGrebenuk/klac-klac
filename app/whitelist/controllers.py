from aiohttp import web

# POST /api/whitelist
from app.whitelist import schemas
from app.whitelist.domain.entity import WhiteList
from app.whitelist.dto import CreateWhiteListDto


async def promote_driver(request, validator, whitelist_mapper, driver_mapper):
    body = await request.json()

    whitelist_dt = CreateWhiteListDto(
        driver_id=body.get('driver_id'),
        passenger_id=request.get('user_id'),
    )
    validator.validate(whitelist_dt, schemas.CreateWhiteListSchema)

    await driver_mapper.get_one_by(user_id=whitelist_dt.driver_id)

    whitelist = WhiteList(driver_id=whitelist_dt.driver_id, passenger_id=whitelist_dt.passenger_id)

    await whitelist_mapper.create(whitelist)

    return web.json_response({})