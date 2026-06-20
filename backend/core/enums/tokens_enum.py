from datetime import timedelta
from enum import Enum


class ActionTokenEnum(Enum):
    ACTIVATE = ('activate', timedelta(hours=24))
    RECOVERY = ('recovery', timedelta(minutes=30))
    ACCESS = ('access', timedelta(minutes=15))
    SOCKET = ('socket', timedelta(minutes=30))

    def __init__(self, token_type: str, lifetime: timedelta):
        self.token_type = token_type
        self.lifetime = lifetime