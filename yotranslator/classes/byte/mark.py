class Mark:
    """метка байтового кода"""

    def __init__(self, value):
        """инициализация метки"""
        self.value = value
        self.cell = 0

    def set_cell(self, cell):
        self.cell = cell

    def get_size(self):
        return 0

    def __str__(self):
        return f"{self.cell} {self.value}"

    def __repr__(self):
        return self.__str__()
