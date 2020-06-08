from PyQt5.QtGui import QTextCharFormat, QColor


class FormatType:

    def __init__(self, highlighter, kind):
        self.expression = highlighter.expressions[kind]
        self.style = QTextCharFormat()
        self.style.setForeground(QColor(*highlighter.styles[kind]["color"]))

    def __str__(self):
        return f"{self.expression}"

    def __repr__(self):
        return self.__str__()
