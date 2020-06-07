from PyQt5.QtWidgets import QMainWindow, QFileSystemModel
from PyQt5 import uic
import os
import webbrowser


class Editor(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("yostructer.ui", self)
        self.file_system = QFileSystemModel()
        self.file_system.setRootPath(os.getcwd())
        self.directories.setModel(self.file_system)
        self.directories.setRootIndex(self.file_system.index(os.getcwd()))
        self.directories.doubleClicked.connect(self.open_file)
        self.help_button.triggered.connect(self.help_link)

    def open_file(self, item):
        path = self.file_system.filePath(item)
        last, package = path.split("/")[-1], "/".join(path.split("/")[:-1])

        if last.endswith(".yostruct"):
            path_name = path[:-9]
            path_html = path_name + ".html"
            self.load_text(path, self.yostruct_area)
            if os.path.exists(path_html):
                self.load_text(path_html, self.html_area)
        elif last.endswith(".html"):
            self.load_text(path, self.html_area)

    @staticmethod
    def load_text(path, area):
        with open(path, "r", encoding="utf-8") as infile:
            text = infile.read()
        area.setPlainText(text)

    def help_link(self):
        link = "https://github.com/PenzaStreetGames/Yo/wiki/" \
               "Yo-Struct-Руководство-пользователя"
        webbrowser.open(link)
