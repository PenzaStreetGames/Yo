import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor, \
    QBrush, QIcon
from PyQt5.QtCore import QRegularExpression, Qt, QSize


class Editor(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("yocode.ui", self)
        self.highlighter = Highlighter(self.CodeArea.document())
        self.CodeArea.textChanged.connect(self.highlighter.color)
        self.setWindowIcon(QIcon("YoCode.png"))
        self.setWindowTitle("Yo Code")


class Highlighter(QSyntaxHighlighter):

    def __init__(self, document):
        super().__init__(document)
        expression = QRegularExpression(".")
        self.colored_document = document
        self.text_format = QTextCharFormat()
        self.text_format.setFontWeight(QFont.Bold)
        self.text_format.setFont(QFont("Consolas"))
        self.text_format.setForeground(Qt.red)
        self.text_format.setFontPointSize(15)
        self.other_format = QTextCharFormat()
        self.other_format.setFontWeight(QFont.Bold)
        self.other_format.setFont(QFont("Consolas"))
        self.other_format.setForeground(Qt.blue)
        self.other_format.setFontPointSize(15)

    def color(self):
        self.highlightBlock(self.colored_document.toPlainText())

    def highlightBlock(self, text):
        print("aaa")
        for i in range(0, len(text), 2):
            self.setFormat(i, 1, self.text_format)
            self.setFormat(i + 1, 1, self.other_format)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = Editor()
    editor.show()
    sys.exit(app.exec_())
