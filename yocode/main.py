import sys
import re
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, \
    QMessageBox
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor, \
    QBrush, QIcon
from PyQt5.QtCore import Qt, QSize
from yocode.constants import *
from yocode.format_objects import get_format_types
import subprocess


class Editor(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("yocode.ui", self)
        self.highlighter = Highlighter(self.CodeArea.document())
        self.CodeArea.textChanged.connect(self.highlighter.color)
        self.open_button.triggered.connect(self.load)
        self.save_button.triggered.connect(self.save)
        self.exit_button.triggered.connect(self.close)
        self.build_button.triggered.connect(self.compile)
        self.setWindowIcon(QIcon("YoCode.png"))
        self.setWindowTitle("Yo Code")
        self.filename_placeholder = "Выберите файл для редактирования"
        self.file = "Выберите файл для редактирования"

    def load(self):
        dialog = QFileDialog(self)
        options = dialog.Options()
        filename, _ = dialog.getOpenFileName(self,
                                             "Открыть",
                                             "",
                                             "Yo Program Text Files (*.yotext)",
                                             options=options)
        if filename:
            self.file = filename
            self.filename.setText(filename.split("/")[-1])
            with open(self.file, mode="r", encoding="utf-8") as infile:
                self.CodeArea.setText(infile.read())

    def save(self):
        dialog = QFileDialog(self)
        options = dialog.Options()
        filename, _ = dialog.getSaveFileName(self,
                                             "Сохранить",
                                             "",
                                             "Yo Program Text Files (*.yotext)",
                                             options=options)
        if filename:
            self.file = filename
            self.filename.setText(filename.split("/")[-1])
            with open(self.file, mode="w", encoding="utf-8") as outfile:
                outfile.write(self.CodeArea.toPlainText())

    def compile(self):
        if self.file == self.filename_placeholder:
            self.statusbar.showMessage("Выберите или сохраните файл для сборки")
            return
        file_address = self.file.replace("/", "\\")
        process = f"python ..\\yotranslator\\main.py -path {file_address} " \
            f"-mode editor"
        result = str(subprocess.check_output(process))
        self.statusbar.showMessage(f"Файл собран в {result}")



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


if __name__ == '__main__':
    command = r"python ..\yotranslator\main.py -path E:\PenzaStreetCompany\Python\-Yo-\yocode\hello_world.yotext -mode editor"
    result = subprocess.check_output(command)
    print(result)
    app = QApplication(sys.argv)
    editor = Editor()
    editor.show()
    sys.exit(app.exec_())
