from yotranslator.classes.byte.program import Program
from yotranslator.classes.binary.binary_program import BinaryProgram
from yotranslator.stages.translate import translate
from yotranslator.stages.assembly.get_vir_commands import get_vir_commands
from yotranslator.stages.assembly.get_relative_addresses import \
    get_relative_addresses
from yotranslator.stages.assembly.get_binary_code import get_binary_code
from yotranslator.stages.assembly.write_file import write_file


if __name__ == '__main__':
    file = input()
    stores = []
    with open(f"{file}.yotext", "r", encoding="utf-8") as infile:
        result = translate(infile.read())
    print("\nСинтаксическое дерево программы:\n")
    print(result[0])

    program = Program([])
    commands = get_vir_commands(result[0])
    for command in commands:
        program.add(command)
    print("\nНабор байтовых команд:\n")
    print(program)

    get_relative_addresses(program)
    print("\nС абсолютными адресами:\n")
    print(program)

    binary_program = BinaryProgram()
    get_binary_code(program, binary_program)
    print("\nБинарный код:\n")
    print(binary_program)

    binary_program.set_tape()
    content = write_file(file, binary_program.tape)
    print(f"\nСодержимое файла {file}.yovc:\n")
    print(*content)
