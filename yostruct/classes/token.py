class Token:

    def __init__(self, name, category, string):
        self.name = name
        self.category = category
        self.string = string

    def add_symbol(self, symbol):
        self.name += symbol

    def __str__(self):
        return self.name
