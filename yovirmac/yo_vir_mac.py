from yovirmac.modules.constants import *
from yovirmac.modules.tape_control import setting, view
from yovirmac.modules.segment_control import find, change, show
from yovirmac.modules.types_control import read, display
from yovirmac.modules.upper_commands import (comparison, console, jumps, logic,
                                             math, objects, other, stack)
import yovirmac.modules.constants as constants

def run(path):
    constants.mode = "console"
    # надо: сделать запуск через аргументы консоли
    execute(path)
def execute(path, debug=False):
    """Запускает исполнение программы"""
    setting.initialisation(path)
    if debug:
        program = find.attribute(seg_links["system"], "main_program")
        show.program_code(program)
    target_cell = find.attribute(seg_links["system"], "target_cell")
    # потом: сделать проверку на прекращение исполнения главной программой
    if constants.mode == "console":
        while target_cell != 0:
            execute_command(target_cell, debug=debug)
            target_cell = find.attribute(seg_links["system"], "target_cell")
    elif constants.mode == "editor":
        return target_cell


def next_command(target_cell, debug=False):
    """Используется в редакторе для перехода от команде к команде"""
    execute_command(target_cell, debug=debug)
    target_cell = find.attribute(seg_links["system"], "target_cell")
    return target_cell


def execute_command(cell, debug=False):
    """Выполняет команду в консольном режиме"""
    command_name, args = read.command_with_args(cell)
    if debug:
        name_num = find.attribute(seg_links["system"], "target_namespace")
        view.namespace_items(name_num)
        display.command_with_args(cell)
    executing_list[command_name](*args)
    cell_now = find.attribute(seg_links["system"], "target_cell")
    if cell == cell_now:
        change.target_cell(cell, args)


executing_list = [
    jumps.End,
    jumps.Jump,
    jumps.Jump_if,
    objects.Create,
    objects.Find,
    objects.Equate,
    objects.Length,
    objects.Sub_object,
    console.Input,
    console.Output,
    stack.Push,
    stack.Pop,
    stack.Call,
    stack.Return,
    logic.Not,
    logic.And,
    logic.Or,
    logic.Xor,
    math.Negative,
    math.Add,
    math.Increment,
    math.Decrement,
    math.Subtract,
    math.Multiply,
    math.Divide,
    math.Modulo,
    comparison.Equal,
    comparison.Great,
    comparison.Less,
    other.No_operation
]

if __name__ == '__main__':
    path = input()
    constants.mode = "console"
    # надо: сделать запуск через аргументы консоли
    execute(path)
