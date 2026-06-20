from enum import Enum


class RegexEnum(Enum):
    NAME = (
        r'^[A-ZА-ЯІЇЄҐ][a-zA-Zа-яА-ЯіїєґІЇЄҐʼ\'-]{1,54}$',
        'Name must start with an uppercase letter and contain 2-55 characters.',
    )

    def __init__(self, pattern: str, message: str):
        self.pattern = pattern
        self.message = message