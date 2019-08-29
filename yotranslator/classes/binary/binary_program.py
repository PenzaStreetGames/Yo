class BinaryProgram:
    """байтовая программа"""

    def __init__(self):
        """инициализация программы"""
        self.binary = []
        self.next_cell = 0
        self.tape = ""

    def add_cell(self, cell):
        """добавление ячейки"""
        self.binary += [cell]
        cell.cell = self.next_cell
        self.next_cell += 1

    def add_cells(self, *cells):
        """добавление ячеек"""
        for cell in cells:
            self.binary += [cell]
            cell.set_cell(self.next_cell)
            self.next_cell += 1

    @staticmethod
    def rjust(num):
        """дополнение нулями в записи до 32 знаков"""
        return num.rjust(32, "0")

    @staticmethod
    def bin(num):
        """преобразование в двоичное число"""
        res = ""
        while num > 1:
            sign = num % 2
            res = str(sign) + res
            num //= 2
        res = str(num) + res
        return res

    @staticmethod
    def dec(cell):
        """преобразование в десятичное число"""
        number, factor = 0, 1
        for i in range(7, -1, -1):
            if cell[i]:
                number += factor
            factor *= 2
        return number

    def set_tape(self):
        """получение ленты памяти из всех ячеек программы"""
        result = ""
        for cell in self.binary:
            result += self.rjust(self.bin(cell.value))
        self.tape = result

    def __str__(self):
        return "\n".join(map(str, self.binary))
