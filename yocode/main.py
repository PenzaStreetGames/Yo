import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtGui import QSyntaxHighlighter


class Editor(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("yocode.ui", self)
        highlighter = Highlighter(self.CodeArea.document())


class Highlighter(QSyntaxHighlighter):

    def __init__(self, document):
        super().__init__(document)

    def highlightBlock(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = Editor()
    editor.show()
    sys.exit(app.exec_())
