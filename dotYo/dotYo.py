import zipfile


def create_yo_archive(name):
    """Создаёт архив .yo с заданным именем. Файлы .yotext и .yovc """
    with zipfile.ZipFile(name + ".yo", 'w') as myzip:
        with myzip.open(f"{name}.yotext", 'w') as f:
            f.write(b"")
        with myzip.open(f"{name}.yovc", 'w') as f:
            f.write(b"")


def write_yotext(name, text):
    """Записывает текст программы в заданный файл yo/yotext"""
    with zipfile.ZipFile(name + ".yo", 'w') as myzip:
        with myzip.open(name + ".yotext", 'w') as f:
            f.write(bytes(text, encoding="utf-8"))


def write_yovc(name, b):
    """Записывает двоичную запись программы в заданный файл yo/yovc"""
    with zipfile.ZipFile(name + ".yo", 'a') as myzip:
        with myzip.open(name + ".yovc", 'w') as f:
            f.write(b)


def get_yotext(name):
    with zipfile.ZipFile(name + ".yo", 'r') as myzip:
        with myzip.open(name + ".yotext", 'r') as f:
            return f.read().decode(encoding="utf-8")


def get_yovc(name):
    with zipfile.ZipFile(name + ".yo", 'r') as myzip:
        with myzip.open(name + ".yovc", 'r') as f:
            return f.read()


if __name__ == '__main__':
    filename = input()
    create_yo_archive(filename)
    write_yotext(filename, "print(1)")
    write_yovc(filename, b"1")
