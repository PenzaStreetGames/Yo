from yovirmac.modules.constants import *
from yovirmac.modules.tape_control import setting
from yovirmac.modules.segment_control import find, change, show
from yovirmac.modules.types_control import read
from yovirmac.modules.upper_commands import *


def execute(path, debug=False):
    setting.initialisation(path)
    if debug:
        program = find.attribute(seg_links["system"], "main_program")
        show.program_code(program)
    target_cell = find.attribute(seg_links["system"], "target_cell")
    # потом: сделать проверку на прекращение исполнения главной программой
    while target_cell != 0:
        execute_command(target_cell)
        target_cell = find.attribute(seg_links["system"], "target_cell")


def execute_command(cell):
    command_name, args = read.command_with_args(cell)
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
    objects.Subobject,
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
    # надо: сделать запуск через аргументы консоли
    execute("path")
