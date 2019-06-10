class TokenError(Exception):
    """Ошибка считывания токена"""
    pass


class YoSyntaxError(Exception):
    """Синтаксическая ошибка языка"""
    pass


class YoMachineError(Exception):
    """Ошибка машинного перевода"""
    pass