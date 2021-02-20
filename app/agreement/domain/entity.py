from dataclasses import dataclass

from app.utils.mapper import Entity


@dataclass
class Agreement(Entity):
    id: str
    driver_id: str
    passenger_id: str