from dataclasses import dataclass


@dataclass
class CreateAgreementDto:
    id: str
    driver_id: str
    order_id: str
