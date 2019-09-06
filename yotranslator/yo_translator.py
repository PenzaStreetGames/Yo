from yotranslator.classes.byte.program import Program
from yotranslator.classes.byte.command import Command
from yotranslator.classes.binary.binary_program import BinaryProgram
from yotranslator.stages.translate import translate
from yotranslator.stages.assembly.get_vir_commands import get_vir_commands
from yotranslator.stages.assembly.get_relative_addresses import \
    get_relative_addresses
from yotranslator.stages.assembly.get_binary_code import get_binary_code
from yotranslator.stages.assembly.get_bytes import get_bytes
import yotranslator.functions.highlight as highlight
from yopacker import yo_packer as packer
from argparse import ArgumentParser


def compile_file(filename, language, mode="main"):
    if filename.endswith(".yo"):
        program = packer.read_yotext(filename)
    else:
        with open(filename, "r", encoding="utf-8") as infile:
            program = infile.read()

    byte_array = compile_program(program, language, mode)

    if filename.endswith(".yo"):
        packer.write_archive(filename, yovm=byte_array)
    else:
        with open(f"{filename}.yovm", "wb") as file:
            file.write(byte_array)

    if mode == "main":
        print(f"\nСодержимое файла {filename}.yovm:\n")
        print(*byte_array)

    return f"{filename}.yovm"


def compile_program(program, language, mode="main"):
    result = translate(program, language)
    if mode == "main":
        print("\nСинтаксическое дерево программы:\n")
        print(result[0])

    program = Program([])
    commands = get_vir_commands(result[0])
    commands += [Command("End")]
    for command in commands:
        program.add(command)
    if mode == "main":
        print("\nНабор байтовых команд:\n")
        print(program)

    get_relative_addresses(program)
    if mode == "main":
        print("\nС абсолютными адресами:\n")
        print(program)

    binary_program = BinaryProgram()
    get_binary_code(program, binary_program)
    if mode == "main":
        print("\nБинарный код:\n")
        print(binary_program)

    binary_program.set_tape()
    byte_array = get_bytes(binary_program.tape)
    return byte_array


if __name__ == '__main__':
    path, lang = input(), input()
    filename = compile_file(path, language=lang, mode="main")
