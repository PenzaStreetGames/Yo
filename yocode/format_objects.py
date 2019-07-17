from PyQt5.QtGui import QTextCharFormat, QColor
from yocode.constants import *


class FormatType:

    def __init__(self, kind):
        self.expression = expressions[kind]
        self.style = QTextCharFormat()
        self.style.setForeground(QColor(*styles[kind]["color"]))


def get_format_types():
    result = []
    for style in groups:
        result += [FormatType(style)]
    return result
