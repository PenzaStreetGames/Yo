class Token:

    def __init__(self, name, category, line):
        self.name = name
        self.category = category
        self.line = line
        if name[0] in {"\"", "\'", "`"}:
            self.quote = True
            self.quote_type = name[0]
        else:
            self.quote = False
            self.quote_type = ""
        self.comment = True if name[0] == "#" else False

    def add_symbol(self, symbol):
        self.name += symbol

    def __str__(self):
        if self.name == "\n":
            name = "\"\\n\""
        elif self.category == "space":
            name = f"\"{self.name}\""
        else:
            name = f"\"{self.name}\""
        return f"{self.category} {name}"

    def __repr__(self):
        return self.__str__()
