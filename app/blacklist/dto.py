from dataclasses import dataclass


@dataclass
class CreateBlackListDto:
    ban_driver_id: str
    passenger_id: str
