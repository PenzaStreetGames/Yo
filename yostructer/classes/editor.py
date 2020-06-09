from PyQt5.QtWidgets import QMainWindow, QFileSystemModel, QInputDialog
from yostructer.classes.html_highlighter import HtmlHighlighter
from yostructer.classes.yostruct_highlighter import YoStructHighlighter
from PyQt5 import uic
import os
import webbrowser
import json


class Editor(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("yostructer.ui", self)
        # File System
        self.file_system = QFileSystemModel()
        self.file_system.setRootPath(os.getcwd())
        self.directories.setModel(self.file_system)
        self.directories.setRootIndex(self.file_system.index(os.getcwd()))
        self.directories.doubleClicked.connect(self.explorer_double_click)
        # Code Areas
        self.html_highlighter = HtmlHighlighter(self.html_area.document())
        self.html_area.textChanged.connect(self.html_highlighter.color)
        self.yostruct_highlighter = YoStructHighlighter(
            self.yostruct_area.document())
        self.yostruct_area.textChanged.connect(self.yostruct_highlighter.color)
        # Toolbar Buttons
        self.exit_action.triggered.connect(self.close)
        self.browser_action.triggered.connect(self.open_in_browser)
        self.help_action.triggered.connect(self.help_link)
        # Buttons
        self.browser_button.clicked.connect(self.open_in_browser)
        # Variables
        self.settings = {}
        self.load_settings()
        self.target_yostruct = ""
        self.target_html = ""
        self.target_file = ""
        self.target_path = ""
        self.style = "pretty"
        if self.settings["last_file"]:
            self.open_file(self.settings["last_file"])

    def create_new_file(self):
        pass

    def explorer_double_click(self, item):
        path = self.file_system.filePath(item)
        self.open_file(path)

    def open_file(self, path):
        last, package = path.split("/")[-1], "/".join(path.split("/")[:-1])

        if last.endswith(".yostruct") or last.endswith(".html"):
            if last.endswith(".yostruct"):
                self.target_path = path[:-9]
            elif last.endswith(".html"):
                self.target_path = path[:-5]
            self.target_yostruct = self.target_path + ".yostruct"
            self.target_html = self.target_path + ".html"
            self.target_file = self.target_path.split("/")[-1]
            if not os.path.exists(self.target_yostruct):
                with open(self.target_yostruct, "w", encoding="utf-8") as infile:
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
