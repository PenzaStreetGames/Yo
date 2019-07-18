from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, \
    QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from yocode.classes.highlighter import Highlighter
from yotranslator import main as translator
import yovirmac.modules.constants as constants
import yovirmac.main as virtual_machine
import traceback
import webbrowser


class Editor(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("yocode.ui", self)
        self.code_highlighter = Highlighter(self.CodeArea.document())
        self.CodeArea.textChanged.connect(self.code_highlighter.color)
        self.open_button.triggered.connect(self.load)
        self.save_button.triggered.connect(self.save)
        self.exit_button.triggered.connect(self.close)
        self.build_button.triggered.connect(self.compile)
        self.help_button.triggered.connect(self.help_link)
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

    def help_link(self):
        link = "https://github.com/PenzaStreetGames/Yo/wiki"
        webbrowser.open(link)

    def compile(self):
        self.clean_data(self.console)
        if self.file == self.filename_placeholder:
            self.statusbar.showMessage("Выберите или сохраните файл для сборки")
            return
        self.save_file()
        path = self.file.replace(".yotext", "")
        try:
            result = translator.compile_program(path, mode="editor")
        except Exception as error:
            self.show_data(self.console, "Ошибка компиляции:")
            trace = traceback.format_exception(error.__class__, error,
                                               error.__traceback__)
            self.show_data(self.console, "".join(trace))
            return
        self.statusbar.showMessage(f"Файл собран в {result}")
        return result

    def compile_and_run(self):
        self.clean_data(self.console)
        file = self.compile()
        if file is None:
            return
        self.save_file()
        path = file.replace(".yotext", ".yovc")
        constants.editor = self
        constants.mode = "editor"
        target_cell = virtual_machine.execute(path)
        while target_cell != 0:
            try:
                target_cell = virtual_machine.next_command(target_cell)
            except Exception as error:
                self.show_data(self.console, "Ошибка исполнения:")
                trace = traceback.format_exception(error.__class__, error,
                                                   error.__traceback__)
                self.show_data(self.console, "".join(trace))
                return
            if constants.input_data:
                self.show_data(self.console, constants.input_data)
                constants.input_data = []
            if constants.output_data:
                self.show_data(self.console, constants.output_data)
                constants.output_data = []

    def show_data(self, widget, data):
        text = widget.toPlainText()
        if type(data) == str:
            if text:
                string = text + "\n" + data
            else:
                string = data
        elif type(data) == list:
            if text:
                string = text + "".join(["\n" + string for string in data])
            else:
                string = "\n".join(data)
        else:
            return
        widget.setText(string)

    def clean_data(self, widget):
        widget.setText("")

    def save_file(self):
        with open(self.file, mode="w", encoding="utf-8") as outfile:
            outfile.write(self.CodeArea.toPlainText())
