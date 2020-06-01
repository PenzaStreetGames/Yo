class BaseYoStructError(Exception):
    """Базовая ошибка YoStruct"""


class StructSyntaxError(BaseYoStructError):
    """Синтаксическая ошибка YoStruct"""


class StructBuildError(BaseYoStructError):
    """Ошибка построения дерева"""


class HTMLTrasformError(BaseYoStructError):
    """Ошибка преобразования в HTML"""
