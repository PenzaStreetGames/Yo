from PyQt5.QtGui import QTextCharFormat, QColor
from yocode.constants import *
from yotransliteration import transliterator



class FormatType:

    def __init__(self, kind, lang):

        # self.expression = ValidExpressions.get(lang)[kind] Здесь я помещал сгенерированные регулярки
        self.style = QTextCharFormat()
        self.style.setForeground(QColor(*styles[kind]["color"]))


def get_format_types(lang):
    result = []
    for style in groups:
        result += [FormatType(style, lang)]
    return result
