from yotranslator.classes.byte.program import Program
from yotranslator.classes.binary.binary_program import BinaryProgram
from yotranslator.stages.translate import translate
from yotranslator.stages.assembly.get_vir_commands import get_vir_commands
from yotranslator.stages.assembly.get_relative_addresses import \
    get_relative_addresses
from yotranslator.stages.assembly.get_binary_code import get_binary_code
from yotranslator.stages.assembly.write_file import write_file
import yotranslator.functions.highlight as highlight


def compile_program(filename, mode="main"):
    with open(f"{filename}.yotext", "r", encoding="utf-8") as infile:
        result = translate(infile.read())
    if mode == "main":
        print("\nСинтаксическое дерево программы:\n")
        print(result[0])
    elif mode == "edit":
        highlight.make_hint(filename)
        return

    program = Program([])
    commands = get_vir_commands(result[0])
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
    content = write_file(filename, binary_program.tape)
    if mode == "main":
        print(f"\nСодержимое файла {filename}.yovc:\n")
        print(*content)
    return f"{filename.rstrip('.yotext')}.yovc"


if __name__ == '__main__':
    file = input()
    compile_program(file, mode="edit")
