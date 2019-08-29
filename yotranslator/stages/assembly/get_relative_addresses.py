from yotranslator.modules.errors import *
from yotranslator.modules.constants import *
from yotranslator.classes.byte.command import Command
from yotranslator.classes.byte.mark import Mark


def get_relative_addresses(program):
    """замена ссылок на относительные адреса"""
    links = []
    for command in program.commands:
        if isinstance(command, Command):
            args = list(filter(lambda arg: arg.arg_type == "lnk",
                               command.args))
            links += args
        elif isinstance(command, Mark):
            links += [command]
    for i in range(len(links)):
        link = links[i]
        link_sign = link.value[:1]
        link_name = link.value[1:]
        if link_sign == "#" or link_sign == "*":
            continue
        elif link_sign == "^":
            if link_name == "rubbish":
                link.arg_type = "non"
                link.value = 0
                continue
            need_mark = "#" if link_name in special_links else "*"
            step = -1 if link_name == "cycle_begin" else 1
            begin_link = i - 1 if step == -1 else i + 1
            end_link = len(links) if step == 1 else -1
            j = 0
            for j in range(begin_link, end_link, step):
                other_link = links[j]
                if type(other_link.value) != str:
                    continue
                other_sign = other_link.value[:1]
                other_name = other_link.value[1:]
                if other_sign == need_mark and link_name == other_name:
                    link.value = other_link.cell
                    break
                elif other_sign == need_mark and (link_name == "next_branch" and
                      other_name in ["branch_begin", "branching_end"]):
                    link.value = other_link.cell
                    break
            if j == end_link:
                if end_link == 0:
                    raise YoSyntaxError("Неправильное использование continue")
                elif end_link == len(links):
                    raise YoSyntaxError("Неправильное использование break")
    program.commands = list(filter(lambda command: isinstance(command, Command),
                                   program.commands))
    for i in range(len(links)):
        link = links[i]
        if type(link.value) != str:
            continue
        link_sign = link.value[:1]
        link_name = link.value[1:]
        if link_sign == "*":
            link.value = 0
        elif link_sign == "^":
            if link_name == "rubbish":
                link.arg_type = "non"
                link.value = 0