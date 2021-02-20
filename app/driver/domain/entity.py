from dataclasses import dataclass

from app.utils.mapper import Entity


@dataclass
class Driver(Entity):
    id: str
    user_id: str
    car_image: str