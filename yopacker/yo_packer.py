import zipfile
import os.path


def exists_yo_archive(path):
    """Проверяет наличие файла в директории"""
    if os.path.exists(path):
        return True
    else:
        return False


def create_yo_archive(path):
    """Создаёт архив .yo с заданным именем. Файлы .yotext и .yovm """
    name = get_filename(path)
    with zipfile.ZipFile(path, 'w') as myzip:
        with myzip.open(f"{name}.yotext", 'w') as f:
            f.write(b"")
        with myzip.open(f"{name}.yovm", 'w') as f:
            f.write(b"")


def write_yotext(path, text):
    """Записывает текст программы в заданный файл yo/yotext"""
    name = get_filename(path)
    with zipfile.ZipFile(path, 'w') as myzip:
        with myzip.open(f"{name}.yotext", 'w') as f:
            f.write(bytes(text, encoding="utf-8"))


def write_yovm(path, binary):
    """Записывает двоичную запись программы в заданный файл yo/yovm"""
    name = get_filename(path)
    with zipfile.ZipFile(path, 'w') as myzip:
        with myzip.open(f"{name}.yovm", 'w') as f:
            f.write(binary)


def read_yotext(path):
    """Возвращает текст программы из данного файла yo/yotext"""
    name = get_filename(path)
    with zipfile.ZipFile(path, 'r') as myzip:
        with myzip.open(f"{name}.yotext", 'r') as f:
            return f.read().decode("utf-8")


def read_yovm(path):
    """Возвращает двоичную запись программы из данного файла yo/yovm"""
    name = get_filename(path)
    with zipfile.ZipFile(path, 'r') as myzip:
        with myzip.open(f"{name}.yovm", 'r') as f:
            return f.read()


def get_filename(path):
    file_name = path.split("/")[-1]
    if file_name.endswith(".yo"):
        file_name = file_name[:-3]
    return file_name


if __name__ == '__main__':
    filename = input()
    create_yo_archive(filename)
    write_yotext(filename, "print(1)")
    write_yovm(filename, b"1")
