import sys
import os
import re
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, \
    QMessageBox
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor, \
    QBrush, QIcon
from yocode.constants import *
from yocode.format_objects import get_format_types
from yotranslator import main as translator
import yovirmac.modules.constants as constants
import yovirmac.main as virtual_machine


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
        self.build_and_run_button.triggered.connect(self.compile_and_run)
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
        path = self.file.replace(".yotext", "")
        result = translator.compile_program(path, mode="editor")
        self.statusbar.showMessage(f"Файл собран в {result}")
        return result

    def compile_and_run(self):
        file = self.compile()
        if file is None:
            return
        path = file.replace(".yotext", ".yovc")
        constants.editor = editor
        constants.mode = "editor"
        try:
            target_cell = virtual_machine.execute(path)
        except Exception as error:
            """text = self.errors.toPlainText()
            self.error.setPlainText(text + str(error))"""
            print(error)
            return
        while target_cell != 0:
            target_cell = virtual_machine.next_command(target_cell)
            """if virtual_machine.input_data:
                text = self.console.toPlainText()
                self.console.setPlainText(
                    text + ["\n" + string for string in
                            virtual_machine.input_data])
                virtual_machine.input_data = []"""
            print(constants.output_data)
            if constants.output_data:
                text = self.console.toPlainText()
                string = text + "".join(["\n" + string for string in
                                         constants.output_data])
                print(string)
                self.console.setText(string)
                constants.output_data = []


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
    app = QApplication(sys.argv)
    editor = Editor()

    file = "E:/PenzaStreetCompany/Python/-Yo-/yotranslator/program.yotext"
    path = file.replace(".yotext", ".yovc")
    constants.editor = editor
    constants.mode = "editor"
    try:
        target_cell = virtual_machine.execute(path)
    except Exception as error:
        """text = self.errors.toPlainText()
        self.error.setPlainText(text + str(error))"""
        print(error)
    while target_cell != 0:
        target_cell = virtual_machine.next_command(target_cell)
        print(constants.output_data)
        if constants.output_data:
            constants.output_data = []

    editor.show()
    sys.exit(app.exec_())
