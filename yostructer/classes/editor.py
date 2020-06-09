from PyQt5.QtWidgets import QMainWindow, QFileSystemModel
from yostructer.classes.html_highlighter import HtmlHighlighter
from yostructer.classes.yostruct_highlighter import YoStructHighlighter
from PyQt5 import uic
import os
import webbrowser


class Editor(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("yostructer.ui", self)
        # File System
        self.file_system = QFileSystemModel()
        self.file_system.setRootPath(os.getcwd())
        self.directories.setModel(self.file_system)
        self.directories.setRootIndex(self.file_system.index(os.getcwd()))
        self.directories.doubleClicked.connect(self.open_file)
        # Code Areas
        self.html_highlighter = HtmlHighlighter(self.html_area.document())
        self.html_area.textChanged.connect(self.html_highlighter.color)
        self.yostruct_highlighter = YoStructHighlighter(
            self.yostruct_area.document())
        self.yostruct_area.textChanged.connect(self.yostruct_highlighter.color)
        # Toolbar Buttons
        self.exit_action.triggered.connect(self.close)
        self.help_action.triggered.connect(self.help_link)
        # Buttons
        # Variables
        self.target_yostruct = ""
        self.target_html = ""
        self.target_file = ""
        self.target_path = ""
        self.style = "pretty"

    def open_file(self, item):
        path = self.file_system.filePath(item)
        last, package = path.split("/")[-1], "/".join(path.split("/")[:-1])

        if last.endswith(".yostruct"):
            path_name = path[:-9]
            path_html = path_name + ".html"
            self_name = path_name.split("/")[-1]
            self.load_text(path, self.yostruct_area)
            self.yostruct_file_label.setText(self_name + ".yostruct")
            if os.path.exists(path_html):
                self.load_text(path_html, self.html_area)
        elif last.endswith(".html"):
            path_name = path[:-5]
            path_yostruct = path_name + ".yostruct"
            self.load_text(path, self.html_area)
            if os.path.exists(path_yostruct):
                self.load_text(path_yostruct, self.yostruct_area)

    @staticmethod
    def load_text(path, area):
        with open(path, "r", encoding="utf-8") as infile:
            text = infile.read()
        area.setPlainText(text)

    @staticmethod
    def help_link():
        link = "https://github.com/PenzaStreetGames/Yo/wiki/" \
               "Yo-Struct-Руководство-пользователя"
        webbrowser.open(link)

    @staticmethod
    def clean_data(widget):
        widget.setText("")
