from PyQt5.QtGui import QTextCharFormat, QColor
from yocode.constants import *
from yotransliteration import transliterator


class ValidExpressions:

    expressions = None
    language = None

    @staticmethod
    def get(language):
        if ValidExpressions.language != language:
            expressions_object = expressions.copy()
            for group in exprs_words_default.keys():
                pattern = []
                for key in exprs_words_default[group]:
                    pattern.append(expressions_object[group].format(transliterator.transliterate(key, "en", language)))

                pattern = "".join(pattern)
                expressions_object[group] = pattern
            ValidExpressions.expressions = expressions_object
            ValidExpressions.language = language
        return ValidExpressions.expressions


class FormatType:

    def __init__(self, kind, lang):

        self.expression = ValidExpressions.get(lang)[kind]
        self.style = QTextCharFormat()
        self.style.setForeground(QColor(*styles[kind]["color"]))


def get_format_types(lang):
    result = []
    for style in groups:
        result += [FormatType(style, lang)]
    return result
