import zipfile
import os
from yotranslator.yo_translator import compile_program
from yovirmac.yo_vir_mac import run


def pack(filename):
    with zipfile.ZipFile(filename + ".yo", 'w') as myzip:
        myzip.write(f"{filename}.yotext")
        myzip.write(f"{filename}.yovc")
        myzip.close()


def unpack(filename):
    print(os.listdir())
    z = zipfile.ZipFile(filename + ".yo", 'r')
    # if filename + ".yotext" in os.listdir():
    z.extract(filename + ".yotext")
    # if filename + ".yovc" in os.listdir():
    z.extract(filename + ".yovc")
    z.close()


def get_yotext(path):
    # todo: добавить проверку на последнее редактирование файла .yotext
    if f"{path}.yotext" in os.listdir():
        compile_program(path, "en", mode="1")
        pack(path)
    if f"{path}.yo" not in os.listdir():
        pack(path)
    else:
        unpack(path)
    with open(path + ".yotext", encoding="utf-8") as f:
        text = f.read()
    os.remove(path + ".yotext")
    return text


def get_yovc(path):
    # todo: добавить проверку на последнее редактирование файла .yotext
    compile_program(path, "en", mode="1")
    if f"{path}.yo" not in os.listdir():
        pack(path)
    else:
        unpack(path)
    with open(path + ".yovc", "rb") as f:
        code = f.read()
    os.remove(path + ".yovc")
    return code


def main():
    # print(os.getcwd())
    path = "program"  # input()
    if f"{path}.yotext" in os.listdir():
        compile_program(path, "en", mode="1")
        pack(path)
    if f"{path}.yo" not in os.listdir():
        pack(path)
    else:
        unpack(path)
    print(path + ".yovc")
    run(path + ".yovc")
    # os.remove(path+".yotext")
    os.remove(path + ".yovc")


if __name__ == '__main__':
    print(get_yotext("program"))
