from yotranslator.modules.constants import *


class Argument:
    """аргумент байтовой команды"""

    def __init__(self, arg_type, value):
        """инициализация аргумента"""
        self.arg_type = arg_type
        self.value = value
        self.cell = 0

    def set_cell(self, cell):
        self.cell = cell

    def get_size(self):
        if type(vir_args_size[self.arg_type]) == int:
            return vir_args_size[self.arg_type]
        elif vir_args_size[self.arg_type] == "many":
            if self.arg_type == "str":
                # один закрывающий байт, второй для симметрии
                return len(self.value) + (2 if len(self.value) % 2 == 1 else 1)

    def __str__(self):
        return f"{self.cell} {self.arg_type} {str(self.value)}"

    def __repr__(self):
        return self.__str__()
