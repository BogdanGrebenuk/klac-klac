from dataclasses import dataclass

from app.utils.mapper import Entity


@dataclass
class BlackList(Entity):
    ban_driver_id: str
    passenger_id: str