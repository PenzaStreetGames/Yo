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
    if "temp" not in os.listdir():
        os.mkdir("temp")
    z = zipfile.ZipFile(filename + ".yo", 'r')
    os.chdir("temp")
    try:
        os.mkdir(filename)
    except:
        pass
    os.chdir(filename)
    z.extractall(path=os.getcwd())
    z.close()


print(os.getcwd())
path = input()
compile_program(path, "en", mode="1")
pack(path)
unpack(path)
print(path + ".yovc")
run(path + ".yovc")
