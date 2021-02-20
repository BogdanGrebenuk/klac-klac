
from aiohttp import web

from app.blacklist.domain.entity import BlackList
from app.blacklist.dto import CreateBlackListDto
from app.blacklist import schemas

# POST /api/blacklist
async def ban_driver(request, validator, blacklist_mapper):
    body = await request.json()

    blacklist_dt = CreateBlackListDto(
        ban_driver_id=body.get('ban_driver_id'),
        passenger_id=request.get('user_id'),
    )
    validator.validate(blacklist_dt, schemas.CreateBlackListSchema)

    blacklist = BlackList(ban_driver_id=blacklist_dt.ban_driver_id, passenger_id=blacklist_dt.passenger_id)

    await blacklist_mapper.create(blacklist)

    return web.json_response({})