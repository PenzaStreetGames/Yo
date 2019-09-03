from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, \
    QMessageBox, QActionGroup
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from yocode.classes.highlighter import Highlighter
from yotranslator import yo_translator as translator
import yopacker.yo_packer as packer
import yovirmac.modules.constants as constants
import yovirmac.yo_vir_mac as virtual_machine
from yovirmac.modules.tape_control.add import decode_assembly
import traceback
import webbrowser
import json


class Language:
    pass


class Editor(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("yocode.ui", self)
        self.settings = {}
        self.load_settings()
        self.code_highlighter = Highlighter(self.CodeArea.document(), self.settings["language"])
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

        self.lang_buttons = {
            "en": self.lang_en,
            "ru": self.lang_ru,
            "tt": self.lang_tt
        }
        self.lang_group = QActionGroup(self)
        self.lang_group.addAction(self.lang_ru)
        self.lang_group.addAction(self.lang_en)
        self.lang_group.addAction(self.lang_tt)
        self.lang_group.setExclusive(True)
        self.switch_language(self.settings["language"])

        self.lang_ru.triggered.connect(self.select_ru)
        self.lang_en.triggered.connect(self.select_en)
        self.lang_tt.triggered.connect(self.select_tt)

    def select_en(self):
        self.switch_language("en")

    def select_ru(self):
        self.switch_language("ru")

    def select_tt(self):
        self.switch_language("tt")

    def switch_language(self, language):
        self.settings["language"] = language
        self.dump_settings()
        for lang, button in self.lang_buttons.items():
            button.setChecked(lang == language)
        self.code_highlighter.update_styles(language)
        old_text = self.CodeArea.toPlainText()
        new_text = old_text.replace("\n", " \n")
        self.CodeArea.setPlainText(new_text)
        # self.code_highlighter.color()
        self.CodeArea.setPlainText(old_text)

    def load_settings(self):
        with open("settings.json", "r", encoding="utf-8") as infile:
            self.settings = json.loads(infile.read())

    def dump_settings(self):
        with open("settings.json", "w", encoding="utf-8") as outfile:
            outfile.write(json.dumps(self.settings, indent=2))

    def load(self):
        dialog = QFileDialog(self)
        options = dialog.Options()
        filename, _ = dialog.getOpenFileName(self,
                                             "Открыть",
                                             "",
                                             "Yo Program Package (*.yo)",
                                             options=options)
        if filename:
            self.file = filename
            self.filename.setText(filename.split("/")[-1])
            text = packer.read_yotext(filename)
            self.CodeArea.setText(text)

    def save(self):
        dialog = QFileDialog(self)
        options = dialog.Options()
        filename, _ = dialog.getSaveFileName(self,
                                             "Сохранить",
                                             "",
                                             "Yo Program Package (*.yo)",
                                             options=options)
        if filename:
            self.file = filename
            self.filename.setText(filename.split("/")[-1])
            if not packer.exists_yo_archive(filename):
                packer.create_yo_archive(filename)
            text = self.CodeArea.toPlainText()
            packer.write_archive(filename, yotext=text)

    def help_link(self):
        link = "https://github.com/PenzaStreetGames/Yo/wiki"
        webbrowser.open(link)

    def compile(self):
        self.clean_data(self.console)
        if self.file == self.filename_placeholder:
            self.statusbar.showMessage("Выберите или сохраните файл для сборки")
            return
        text = self.CodeArea.toPlainText()
        packer.write_archive(self.file, yotext=text)
        try:
            result = translator.compile_program(text, language=self.settings["language"], mode="editor")
        except Exception as error:
            self.show_data(self.console, "Ошибка компиляции:")
            trace = traceback.format_exception(error.__class__, error,
                                               error.__traceback__)
            self.show_data(self.console, "".join(trace))
            return
        packer.write_archive(self.file, yovm=result)
        self.statusbar.showMessage(f"Файл собран")
        return result

    def transliterate(self):
        result = self.file
        return result

    def compile_and_run(self):
        self.clean_data(self.console)
        code = self.compile()
        if code is None:
            return
        code = decode_assembly(packer.read_yovm(self.file))
        constants.editor = self
        constants.mode = "editor"
        target_cell = virtual_machine.execute_program(code)
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
