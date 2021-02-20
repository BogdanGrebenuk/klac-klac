from dataclasses import dataclass


@dataclass
class CreateWhiteListDto:
    driver_id: str
    passenger_id: str
