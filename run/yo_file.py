import zipfile
import os
def pack(filename):
    with zipfile.ZipFile(filename+".yo", 'w') as myzip:
        myzip.write(f"{filename}.yotext")
        myzip.write(f"{filename}.yovc")
        myzip.close()
def _open(filename):
    if "temp" not in os.listdir():
        os.mkdir("temp")
    z = zipfile.ZipFile(filename+".yo",'r')
    #z.printdir()
    os.chdir("temp")
    if filename not in os.listdir():
        os.mkdir(filename)
    os.chdir(filename)
    z.extract("1.yotext")
    z.extract("1.yovc")
    #z.extractall()
    z.close()

if __name__ == "__main__":
    path = input("filename ")
    pack(path)
    _open(path)
