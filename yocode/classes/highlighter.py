from PyQt5.QtGui import QSyntaxHighlighter
from yocode.format_objects import get_format_types
from yocode.constants import *
import re


class Highlighter(QSyntaxHighlighter):

    def __init__(self, document):
        super().__init__(document)
        self.colored_document = document
        self.styles = get_format_types()

    def color(self):
        self.highlightBlock(self.colored_document.toPlainText())

    def highlightBlock(self, text):
        for i in range(len(groups)):
            expression = self.styles[i].expression
            style = self.styles[i].style
            for token in re.finditer(expression, text, re.MULTILINE):
                begin = token.start()
                end = token.end()
                length = end - begin
                self.setFormat(begin, length, style)