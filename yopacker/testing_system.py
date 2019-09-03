from yopacker.yo_packer import *


def file_creating():
    create_yo_archive("archive.yo")


def file_existing():
    print(exists_yo_archive(os.getcwd() + "\\archive.yo"))
    create_yo_archive("archive.yo")
    print(exists_yo_archive(os.getcwd() + "\\archive.yo"))


def yotext_working():
    create_yo_archive("archive.yo")
    write_yotext("archive", "print('Hello, World!')")
    print(read_yotext("archive.yo"))


def yovm_working():
    create_yo_archive("archive.yo")
    write_yovm("archive", b"\x03\x05\x06")
    print(read_yovm("archive.yo"))


tests = {
    1: file_creating,
    2: file_existing,
    3: yotext_working,
    4: yovm_working
}

while True:
    number = int(input())
    tests[number]()
