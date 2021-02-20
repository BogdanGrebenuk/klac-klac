from dataclasses import dataclass

from app.utils.mapper import Entity


@dataclass
class Passenger(Entity):
    id: str
    user_id: str
