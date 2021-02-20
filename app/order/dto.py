from dataclasses import dataclass


@dataclass
class CreateOrderDto:
    id: str
    passenger_id: str
    from_: str
    to: str
    status: str
