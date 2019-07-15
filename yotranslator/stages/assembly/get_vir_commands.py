from yotranslator.modules.errors import *
from yotranslator.modules.constants import *
from yotranslator.classes.byte.command import Command
from yotranslator.classes.byte.argument import Argument
from yotranslator.classes.byte.mark import Mark


def get_vir_commands(yo_object):
    """выдать набор байтовых команд для токена"""
    global virtual_commands
    commands = []
    if yo_object.group == "object":
        if yo_object.sub_group == "name":
            commands = [Command("Crt", Argument("str", yo_object.name)),
                        Command("Pop", Argument("lnk", "^a")),
                        Command("Fnd", Argument("lnk", "*a"))]
        elif yo_object.sub_group == "none":
            commands = [Command("Crt", Argument("non", 0))]
        elif yo_object.sub_group == "logic":
            value = 1 if yo_object.name == "true" else 0
            commands = [Command("Crt", Argument("log", value))]
        elif yo_object.sub_group == "number":
            commands = [Command("Crt", Argument("num", int(yo_object.name)))]
        elif yo_object.sub_group == "string":
            commands = [Command("Crt", Argument("str", yo_object.name))]
        elif yo_object.sub_group == "list":
            end_command_args = []
            for i in range(len(yo_object.args)):
                argument = yo_object.args[i]
                commands += get_vir_commands(argument)
                commands += [Command("Pop", Argument("lnk", f"^{i}"))]
                end_command_args += [Argument("lnk", f"*{i}")]
            end_command_args += [Argument("non", 0)]
            commands += [Command("Crt", Argument("lst", 0), *end_command_args)]
    elif yo_object.group == "expression":
        if yo_object.sub_group == "(":
            commands += get_vir_commands(yo_object.args[0])
        elif yo_object.sub_group == "call_expression":
            for child in yo_object.args:
                commands += get_vir_commands(child)
        elif yo_object.sub_group == "index_expression":
            commands += get_vir_commands(yo_object.args[0])
        elif yo_object.sub_group == "branching":
            for branch in yo_object.args:
                commands += [Mark("#branch_begin"),
                             *get_vir_commands(branch),
                             Command("Jmp", Argument("lnk", "^branching_end"))]
            commands += [Mark("#branching_end")]
    elif yo_object.group == "sub_object":
        commands += [*get_vir_commands(yo_object.args[0]),
                     *get_vir_commands(yo_object.args[1])]
        commands += [Command("Pop", Argument("lnk", "^b")),
                     Command("Pop", Argument("lnk", "^a")),
                     Command("Sob", Argument("lnk", "*a"),
                             Argument("lnk", "*b"))]
    elif yo_object.group == "call":
        func_name = yo_object.args[0].name
        func_args = yo_object.args[1].args
        length = len(func_args)
        if func_name == "print":
            if length == 1:
                commands += [*get_vir_commands(yo_object.args[1]),
                             Command("Pop", Argument("lnk", "^a")),
                             Command("Out", Argument("lnk", "*a"))]
            else:
                raise YoSyntaxError(f"Неправильное число аргументов {func_name}"
                                    f" {length}")
        elif func_name == "input":
            if length == 0:
                commands += [Command("Inp")]
            else:
                raise YoSyntaxError(f"Неправильное число аргументов {func_name}"
                                    f" {length}")
        elif func_name == "len":
            if length == 1:
                commands += [*get_vir_commands(yo_object.args[1]),
                             Command("Pop", Argument("lnk", "^a")),
                             Command("Len", Argument("lnk", "*a"))]
            else:
                raise YoSyntaxError(f"Неправильное число аргументов {func_name}"
                                    f" {length}")
        else:
            raise YoSyntaxError(f"Функции не поддерживаются, кроме print, "
                                f"len и input, но не {func_name}")
    elif yo_object.group == "math":
        for child in yo_object.args:
            commands += get_vir_commands(child)
        func = virtual_commands[yo_object.sub_group]
        if func != "Neg":
            commands += [Command("Pop", Argument("lnk", "^b")),
                         Command("Pop", Argument("lnk", "^a")),
                         Command(func, Argument("lnk", "*a"),
                                 Argument("lnk", "*b"))]
        else:
            commands += [Command("Pop", Argument("lnk", "^a")),
                         Command(func, Argument("lnk", "*a"))]
    elif yo_object.group == "comparison":
        for child in yo_object.args:
            commands += get_vir_commands(child)
        func = virtual_commands[yo_object.sub_group]
        commands += [Command("Pop", Argument("lnk", "^b")),
                     Command("Pop", Argument("lnk", "^a")),
                     Command(func, Argument("lnk", "*a"),
                             Argument("lnk", "*b"))]
    elif yo_object.group == "logic":
        for child in yo_object.args:
            commands += get_vir_commands(child)
        func = virtual_commands[yo_object.sub_group]
        if func != "Not":
            commands += [Command("Pop", Argument("lnk", "^b")),
                         Command("Pop", Argument("lnk", "^a")),
                         Command(func, Argument("lnk", "*a"),
                                 Argument("lnk", "*b"))]
        else:
            commands += [Command("Pop", Argument("lnk", "^a")),
                         Command(func, Argument("lnk", "*a"))]
    elif yo_object.group == "equating":
        for child in yo_object.args:
            commands += get_vir_commands(child)
        commands += [Command("Pop", Argument("lnk", "^b")),
                     Command("Pop", Argument("lnk", "^a")),
                     Command("Eqt", Argument("lnk", "*a"),
                             Argument("lnk", "*b"))]
    elif yo_object.group == "interrupt":
        if yo_object.name == "break":
            commands += [Command("Jmp", Argument("lnk", "^cycle_end"))]
        elif yo_object.name == "continue":
            commands += [Command("Jmp", Argument("lnk", "^cycle_begin"))]
        elif yo_object.name == "pass":
            commands += [Command("Nop")]
    elif yo_object.group == "structure_word":
        if yo_object.sub_group in ["if", "elseif"]:
            commands += [*get_vir_commands(yo_object.args[0]),
                         Command("Pop", Argument("lnk", "^a")),
                         Command("Jif", Argument("lnk", "*a"),
                                 Argument("lnk", "^next_branch")),
                         *get_vir_commands(yo_object.args[1])]
        elif yo_object.sub_group == "else":
            commands += [*get_vir_commands(yo_object.args[0])]
        elif yo_object.sub_group == "while":
            commands += [Mark("#cycle_begin"),
                         *get_vir_commands(yo_object.args[0]),
                         Command("Pop", Argument("lnk", "^a")),
                         Command("Jif", Argument("lnk", "*a"),
                                 Argument("lnk", "^cycle_end")),
                         *get_vir_commands(yo_object.args[1]),
                         Command("Jmp", Argument("lnk", "^cycle_begin")),
                         Mark("#cycle_end")]
        commands += [Command("Psh", Argument("lnk", "^rubbish"))]
    elif yo_object.group == "program":
        for child in yo_object.args:
            commands += [*get_vir_commands(child),
                         Command("Pop", Argument("lnk", "^rubbish"))]
    return commands
