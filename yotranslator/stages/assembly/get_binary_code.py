from yotranslator.modules.constants import *
from yotranslator.classes.binary.binary_cell import BinaryCell


def get_binary_code(program, binary_program):
    """превращение байтовых команд и аргументов в числа"""
    for command in program.commands:
        command_type = binary_values["types"]["cmd"]
        command_code = binary_values["commands"][command.name]
        binary_program.add_cells(BinaryCell(command_type),
                                 BinaryCell(command_code))
        for arg in command.args:
            arg_type = binary_values["types"][arg.arg_type]
            binary_program.add_cell(BinaryCell(arg_type))
            if arg.arg_type in type_memory_view["number"]:
                binary_program.add_cell(BinaryCell(arg.value))
            elif arg.arg_type in type_memory_view["symbol_list"]:
                for symbol in arg.value:
                    binary_program.add_cell(BinaryCell(ord(symbol)))
                binary_program.add_cell(BinaryCell(0))
                if len(arg.value) % 2 == 1:
                    binary_program.add_cell(BinaryCell(0))
