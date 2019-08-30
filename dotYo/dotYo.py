import zipfile
import os
import sys
from ..yotranslator.yo_translator import compile_program
from yovirmac.yo_vir_mac import execute

def pack(filename):
    with zipfile.ZipFile(filename+".yo", 'w') as myzip:
        myzip.write(f"{filename}.yotext")
        myzip.write(f"{filename}.yovc")
        myzip.close()

def unpack(filename):
    if "temp" not in os.listdir():
        os.mkdir("temp")
    z = zipfile.ZipFile(filename+".yo",'r')
    os.chdir("temp")
    if filename not in os.listdir():
        os.mkdir(filename)
    os.chdir(filename)
    z.extractall(path=os.getcwd())
    z.close()

path = sys.argv[1]
compile_program("temp/"+path+".yotext")
pack(path)
unpack(path)
execute("temp/"+path+".yovc")
