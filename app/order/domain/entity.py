from dataclasses import dataclass

from app.utils.mapper import Entity


@dataclass
class Order(Entity):
    id: str
    from_: str
    to: str
    status: str
    driver_id: str
    passenger_id: str
    image: str
    geolocation: str