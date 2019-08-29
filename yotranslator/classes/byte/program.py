class Program:
    """программа байтовых команд"""

    def __init__(self, commands):
        """инициализация с загрузкой команд"""
        self.commands = commands
        self.next_cell = 0

    def insert(self, command, place):
        """вставить команду в нужное место"""
        self.commands.insert(command, place)

    def add(self, command):
        """добавить команду"""
        command.set_cell(self.next_cell)
        self.commands += [command]
        self.next_cell += command.get_size()

    def __str__(self):
        return "\n".join(map(str, self.commands))

    def __repr__(self):
        return self.__str__()
