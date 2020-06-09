from PyQt5.QtWidgets import QMainWindow, QFileSystemModel, QInputDialog, \
    QButtonGroup
from yostructer.classes.html_highlighter import HtmlHighlighter
from yostructer.classes.yostruct_highlighter import YoStructHighlighter
from yostruct.yo_struct import convert_yostruct
from yostruct.errors import BaseYoStructError
from PyQt5 import uic
import traceback
import os
import webbrowser
import json


class Editor(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("yostructer.ui", self)
        # Settings
        self.settings = {}
        self.load_settings()
        # File System
        self.file_system = QFileSystemModel()
        self.file_system.setRootPath(os.getcwd())
        self.directories.setModel(self.file_system)
        self.directories.setRootIndex(
            self.file_system.index(os.getcwd() + "/yostruct_files/"))
        self.directories.doubleClicked.connect(self.explorer_double_click)
        # Code Areas
        self.html_highlighter = HtmlHighlighter(self.html_area.document())
        self.html_area.textChanged.connect(self.html_highlighter.color)
        self.yostruct_highlighter = YoStructHighlighter(
            self.yostruct_area.document())
        self.yostruct_area.textChanged.connect(self.yostruct_highlighter.color)
        # Toolbar Buttons
        self.new_file_action.triggered.connect(self.create_new_file)
        self.save_yostruct_action.triggered.connect(self.save_yostruct)
        self.save_html_action.triggered.connect(self.save_html)
        self.save_all_action.triggered.connect(self.save_all)
        self.exit_action.triggered.connect(self.close)
        self.browser_action.triggered.connect(self.open_in_browser)
        self.help_action.triggered.connect(self.help_link)
        # Buttons
        self.browser_button.clicked.connect(self.open_in_browser)
        self.convert_button.clicked.connect(self.convert_yostruct)
        self.convert_open_button.clicked.connect(self.convert_and_open)
        # Radio Buttons
        self.style_group = QButtonGroup(self)
        self.style_group.addButton(self.oneline_style)
        self.style_group.addButton(self.pretty_style)
        self.style_group.addButton(self.rich_style)
        self.style_group.setExclusive(True)
        self.oneline_style.toggled.connect(self.switch_oneline_style)
        self.pretty_style.toggled.connect(self.switch_pretty_style)
        self.rich_style.toggled.connect(self.switch_rich_style)
        self.style_buttons = {
            "oneline": self.oneline_style,
            "pretty": self.pretty_style,
            "rich": self.rich_style,
        }
        self.style_buttons[self.settings["style"]].setChecked(True)
        # Variables
        self.target_yostruct = ""
        self.target_html = ""
        self.target_file = ""
        self.target_path = ""
        self.style = "pretty"
        if self.settings["last_file"] and \
                os.path.exists(self.settings["last_file"]):
            self.open_file(self.settings["last_file"])

    def switch_pretty_style(self):
        self.switch_style("pretty")

    def switch_oneline_style(self):
        self.switch_style("oneline")

    def switch_rich_style(self):
        self.switch_style("rich")

    def switch_style(self, style):
        self.settings["style"] = style
        self.save_settings()

    def convert_and_open(self):
        self.convert_yostruct()
        self.open_in_browser()

    def convert_yostruct(self):
        self.console.setPlainText("")
        if not self.target_file:
            return
        text = self.yostruct_area.toPlainText()
        text = text.replace("\t", "    ")
        self.yostruct_area.setPlainText(text)
        try:
            html = convert_yostruct(text, style=self.settings["style"])
            self.show_console(f"Файл {self.target_html} преобразован")
        except BaseYoStructError as error:
            self.show_console("Ошибка построения структуры:")
            trace = traceback.format_exception(error.__class__, error,
                                               error.__traceback__)
            self.show_console("".join(trace))
            return
        except BaseException as error:
            self.show_console("Ошибка Python:")
            trace = traceback.format_exception(error.__class__, error,
                                               error.__traceback__)
            self.show_console("".join(trace))
            return
        self.html_area.setPlainText(html)
        self.save_all()

    def show_console(self, data):
        text = self.console.toPlainText()
        if type(data) == str:
            string = text + "\n" + data if text else data
        elif type(data) == list:
            string = text + "".join(["\n" + string for string in data])
        else:
            return
        self.console.setPlainText(string)

    def create_new_file(self):
        filename, i = QInputDialog.getText(
            self, "Новый .yostruct", "Введите имя (с разрашением или без)")
        if not filename.endswith(".yostruct"):
            filename = f"{filename}.yostruct"
        with open(filename, "w", encoding="utf-8") as infile:
            infile.write("")
        self.open_file(f"{os.getcwd()}/yostruct_files/{filename}")

    def explorer_double_click(self, item):
        path = self.file_system.filePath(item)
        self.save_all()
        self.open_file(path)

    def open_file(self, path):
        last, package = path.split("/")[-1], "/".join(path.split("/")[:-1])
        if last.endswith(".yostruct"):
            self.target_path = path[:-9]
            self.target_file = self.target_path.split("/")[-1]
            self.target_yostruct = self.target_path + ".yostruct"
            self.target_html = f"{os.getcwd()}/html_files/" \
                f"{self.target_file}.html"
            if not os.path.exists(self.target_yostruct):
                with open(self.target_yostruct, "w",
                          encoding="utf-8") as infile:
                    infile.write("")
            self.load_text(self.target_yostruct, self.yostruct_area)
            self.yostruct_file_label.setText(self.target_file + ".yostruct")
            if not os.path.exists(self.target_html):
                with open(self.target_html, "w", encoding="utf-8") as infile:
                    infile.write("")
            self.load_text(self.target_html, self.html_area)
            self.html_file_label.setText(self.target_file + ".html")
            self.file_name_label.setText(self.target_file)
            self.settings["last_file"] = self.target_yostruct
            self.save_settings()

    def save_all(self):
        self.save_yostruct()
        self.save_html()

    def save_yostruct(self):
        self.save_file("yostruct")

    def save_html(self):
        self.save_file("html")

    def save_file(self, area):
        if area == "yostruct":
            text = self.yostruct_area.toPlainText()
            path = self.target_yostruct
        elif area == "html":
            text = self.html_area.toPlainText()
            path = self.target_html
        else:
            return
        with open(path, "w", encoding="utf-8") as outfile:
            outfile.write(text)

    def load_settings(self):
        with open("settings.json", "r", encoding="utf-8") as infile:
            self.settings = json.loads(infile.read())

    def save_settings(self):
        with open("settings.json", "w", encoding="utf-8") as outfile:
            outfile.write(json.dumps(self.settings, indent=2))

    @staticmethod
    def load_text(path, area):
        with open(path, "r", encoding="utf-8") as infile:
            text = infile.read()
        area.setPlainText(text)

    def open_in_browser(self):
        if self.target_html:
            webbrowser.open("file://" + self.target_html)

    @staticmethod
    def help_link():
        link = "https://github.com/PenzaStreetGames/Yo/wiki/" \
               "Yo-Struct-Руководство-пользователя"
        webbrowser.open(link)

    @staticmethod
    def clean_data(widget):
        widget.setText("")
