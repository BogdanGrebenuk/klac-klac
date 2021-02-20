import uuid

from aiohttp import web

from app.driver.domain.entity import Driver
from app.passenger.domain.entity import Passenger
from app.user.auth.dto import CreateUserDto, AuthenticateUserDto
from app.user.domain.role import UserRole


async def authenticate_user(request, authenticator):
    body = await request.json()

    token = await authenticator.authenticate(
        AuthenticateUserDto(
            email=body.get('email'),
            password=body.get('password')
        )
    )

    return web.json_response({'token': token})


async def register_user(
        request,
        registrar,
        user_mapper,
        user_transformer,
        passenger_mapper,
        driver_mapper
        ):
    body = await request.json()

    user = await registrar.register(
        CreateUserDto(
            id=str(uuid.uuid4()),
            email=body.get('email'),
            password=body.get('password'),
            first_name=body.get('first_name'),
            last_name=body.get('last_name'),
            patronymic=body.get('patronymic'),
            role=body.get('role')
        )
    )

    if user.role == UserRole.PASSENGER.value:
        passenger = Passenger(
            id=user.id,
            user_id=user.id
        )
        user.passenger_id = passenger.id
        await passenger_mapper.create(passenger)
    elif user.role == UserRole.DRIVER.value:
        driver = Driver(
            id=user.id,
            user_id=user.id
        )
        user.driver_id = driver.id
        await driver_mapper.create(driver)

    await user_mapper.create(user)

    return web.json_response(await user_transformer.transform(user))


async def logout_user(request, user_mapper):
    user = await user_mapper.find(request.get('user_id'))

    user.token = None

    await user_mapper.update(user)

    return web.json_response({})
