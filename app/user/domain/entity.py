from dataclasses import dataclass

from app.utils.mapper import Entity


@dataclass
class User(Entity):
    id: str
    first_name: str
    last_name: str
    patronymic: str
    email: str
    password: str
    role: str
    driver_id: str
    passenger_id: str
    token: str = None
