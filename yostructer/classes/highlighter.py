from PyQt5.QtGui import QSyntaxHighlighter
from yostructer.classes.format_type import FormatType
import re


class Highlighter(QSyntaxHighlighter):

    def __init__(self, document):
        super().__init__(document)
        self.colored_document = document
        self.groups = []
        self.expressions = {}
        self.colors = {}
        self.styles = self.get_format_types()

    def color(self):
        self.highlightBlock(self.colored_document.toPlainText())

    def highlightBlock(self, text):
        for i in range(len(self.groups)):
            expression = self.styles[i].expression
            style = self.styles[i].style
            for token in re.finditer(expression, text, re.MULTILINE):
                begin = token.start()
                end = token.end()
                length = end - begin
                self.setFormat(begin, length, style)

    def get_format_types(self):
        result = []
        for style in self.groups:
            result.append(FormatType(self, style))
        return result
