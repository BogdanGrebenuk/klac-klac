from enum import Enum


class PassengerOrderStatus(Enum):
    SEARCHING = 'searching'
    IN_MID_COURSE = 'in_mid_course'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

    @classmethod
    def get_roles(cls):
        return [i.value for i in cls]


class DriverOrderStatus(Enum):
    PENDING = 'pending'
    REJECTED = 'rejected'
    ACCEPTED = 'accepted'

    @classmethod
    def get_roles(cls):
        return [i.value for i in cls]