import zipfile
import os
from yotranslator.yo_translator import compile_program

try: #знаю, так делать не надо
    from yovirmac.yo_vir_mac import run
except:
    pass


def create_yo_archive(name):
    """Создаёт архив .yo с заданным именем. Файлы .yotext и .yovc """
    with zipfile.ZipFile(name + ".yo", 'w') as myzip:
        myzip.write(f"{name}.yotext")
        myzip.write(f"{name}.yovc")


def write_yotext(name, text):
    """Записывает текст программы в заданный файл yo/yotext"""
    # if f"{name}.yo" in os.listdir():
    with zipfile.ZipFile(name + ".yo", 'w') as myzip:
        with myzip.open(name + ".yotext", 'w') as f:
            f.write(text)


def write_yovc(name, b):
    """Записывает двоичную запись программы в заданный файл yo/yovc"""
    # if f"{name}.yo" in os.listdir():
    with zipfile.ZipFile(name + ".yo", 'w') as myzip:
        with myzip.open(name + ".yotext", 'wb') as f:
            f.write(b)


def get_yotext(name):
    with zipfile.ZipFile(name + ".yo", 'r') as myzip:
        with myzip.open(name + ".yotext", 'r') as f:
            return f.read()


def get_yovc(name):
    with zipfile.ZipFile(name + ".yo", 'r') as myzip:
        with myzip.open(name + ".yovc", 'rb') as f:
            return f.read()


if __name__ == '__main__':
    filename = input()
    create_yo_archive(filename)
