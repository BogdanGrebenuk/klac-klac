from enum import Enum


class UserRole(Enum):
    DRIVER = 'driver'
    PASSENGER = 'passenger'

    @classmethod
    def get_roles(cls):
        return [i.value for i in cls]
