import sys
from main import _translate
from mainvm import run
from yo_file import pack,_open
import os
path = sys.argv[1]
pack(path)
_open(path)
_translate(path+".yotext")
run(path+".yovc")=
