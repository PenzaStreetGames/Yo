from yotranslator.modules.errors import *


class BinaryCell:
    """байтовая ячейка"""

    def __init__(self, value):
        """инициализация ячейки"""
        self.cell = 0
        self.value = value
        if type(value) != int:
            raise YoMachineError(f"В ячейку передалось нечисло {value}")

    def set_cell(self, cell):
        """задание номера ячейки"""
        self.cell = cell

    def __str__(self):
        return f"{self.cell} {self.value}"

    def __repr__(self):
        return self.__str__()
