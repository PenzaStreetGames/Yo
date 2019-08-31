from PyQt5.QtGui import QTextCharFormat, QColor
from yocode.constants import *


class FormatType:

    def __init__(self, kind, lang):

        self.expression = get_expression_group(kind, lang)
        self.style = QTextCharFormat()
        self.style.setForeground(QColor(*styles[kind]["color"]))


def get_format_types(lang):
    result = []
    for style in groups:
        result += [FormatType(style, lang)]
    return result


def get_expression_group(group, language):
    if group in translated_groups:
        words = []
        for word in translated_words[group]:
            words += [langpack[word][language]]
            if language != "en":
                words += [langpack[word]["en"]]
        string = [r"\b{}\b".format(word) for word in words]
        string = "|".join(string)
        return string
    else:
        return expressions[group]
