class BaseYoError(Exception):
    """Класс базовой ошибки Ё"""


class TokenError(BaseYoError):
    """Ошибка считывания токена"""


class YoSyntaxError(BaseYoError):
    """Синтаксическая ошибка языка"""


class YoMachineError(BaseYoError):
    """Ошибка машинного перевода"""
