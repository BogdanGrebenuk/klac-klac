from dataclasses import dataclass

from app.utils.mapper import Entity


@dataclass
class WhiteList(Entity):
    driver_id: str
    passenger_id: str