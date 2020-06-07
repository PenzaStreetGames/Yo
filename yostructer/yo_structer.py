from PyQt5.QtWidgets import QApplication
from yostructer.classes.editor import Editor
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = Editor()
    editor.show()
    sys.exit(app.exec_())
