class Command:
    """байтовая команда"""

    def __init__(self, name, *arguments):
        """инициализация команды"""
        self.name = name
        self.args = arguments
        self.cell = 0
        self.size = self.get_size()

    def set_cell(self, cell):
        self.cell = cell
        arg_cell = cell + 2
        for arg in self.args:
            arg.set_cell(arg_cell)
            arg_cell += arg.get_size() + 1

    def get_size(self):
        """длина команды в ячейках"""
        length = 2
        for arg in self.args:
            length += arg.get_size() + 1
        return length

    def __str__(self):
        return f"{self.cell}  {self.name}  " \
               f"{' '.join(map(lambda arg: str(arg), self.args))}"

    def __repr__(self):
        return self.__str__()
