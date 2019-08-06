import zipfile
def pack(filename):
    with zipfile.ZipFile(filename, 'w') as myzip:
        myzip.write(f"{filename}.yotext")
        myzip.write(f"{filename}.yovc")
def open(filename):
    z = zipfile.ZipFile(filename,'r')
    z.extractall()
    #надо:дать транслятору файл .yotext на съедение
