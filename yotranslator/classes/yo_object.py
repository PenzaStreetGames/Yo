from yotranslator.modules.errors import *
from yotranslator.modules.constants import *


class YoObject:
    """объект кода"""

    def __init__(self, parent, func):
        """инициализация объекта"""
        self.parent = parent
        self.func = func
        self.args = []
        self.priority = [group_priority[func["group"]],
                         priority[func["group"]][func["sub_group"]]]
        self.name = func["name"]
        self.sub_group = func["sub_group"]
        self.group = func["group"]
        self.args_number = args_number[self.group][self.sub_group]
        self.commas, self.points = self.get_punctuation()
        self.close = False
        self.indent = 0
        self.inside_indent = 0

    def check_close(self, result):
        """проверка на возможность закрытия"""
        if self.args_number == "no":
            pass
        elif self.args_number == "unary":
            if len(self.args) != 1:
                raise YoSyntaxError(f"Неправильное число аргументов {self}")
        elif self.args_number == "binary" or self.args_number == "binary_right":
            if len(self.args) != 2:
                raise YoSyntaxError(f"Неправильное число аргументов {self}")
        elif self.args_number == "many":
            if not self.close:
                if self.sub_group == "branching":
                    result = self.set_close(result)
                else:
                    raise YoSyntaxError(f"Незакрытое перечисление {self}")
        for arg in self.args:
            result = arg.check_close(result)
            result = arg.set_close(result).copy()
        return result

    def is_close(self):
        """закрыт ли объект для новых аргументов"""
        if self.args_number == "no":
            return len(self.args) == 0
        elif self.args_number == "unary":
            return len(self.args) == 1
        elif self.args_number == "binary":
            return len(self.args) == 2
        elif self.args_number == "many":
            return self.close

    def set_close(self, result):
        """закрытие объекта для новых аргументов"""
        self.close = True
        if result[-1] == self:
            result = result[:-1]
        return result

    def add_arg(self, yo_object):
        """добавление аргумента"""
        self.args += [yo_object]
        yo_object.parent = self

    def remove_arg(self):
        """удаление аргумента"""
        yo_object = self.args.pop()
        return yo_object

    def __str__(self):
        """строковое представление объекта"""
        if self.sub_group == self.name:
            result = self.group
        else:
            result = self.sub_group
        result += " " + self.name
        for arg in self.args:
            result += "\n" + "    " * self.get_nesting(1) + arg.__repr__()
        return result

    def __repr__(self):
        """тоже представление объекта"""
        if self.sub_group == self.name:
            result = self.group
        else:
            result = self.sub_group
        result += " " + self.name
        for arg in self.args:
            result += "\n" + "    " * self.get_nesting(1) + arg.__repr__()
        return result

    def get_nesting(self, number):
        """получить уровень вложенности объекта"""
        if self.parent is not None:
            number = self.parent.get_nesting(number + 1)
        return number

    def set_indent(self, indent, inside=False):
        if not inside:
            if self.group == "structure_word":
                self.parent.set_indent(indent, inside=True)
            self.indent = indent
        else:
            self.inside_indent = indent
            if self.sub_group == "branching":
                self.indent = indent
            elif self.sub_group == "indent_program":
                self.indent = indent
        if self.sub_group == "indent_program":
            if self.parent and self.parent.group == "structure_word":
                self.parent.set_indent(indent, inside=True)
            self.indent = indent
            self.inside_indent = indent

    def get_punctuation(self):
        """получение знаков препинания для токена"""
        if self.sub_group == "indent_program":
            return [";", "\n"], []
        elif self.sub_group == "scopes_program":
            return [";", "\n"], ["}"]
        elif self.sub_group == "oneline_program":
            return [], [";", "\n"]
        elif self.group == "structure_word":
            return [":", "{"], ["}"]
        elif self.group == "interrupt":
            return [], []
        elif self.sub_group == "list":
            return [","], ["]"]
        elif self.sub_group == "call_expression":
            return [","], [")"]
        elif self.sub_group == "index_expression":
            return [], ["]"]
        elif self.sub_group == "branching":
            return ["\n"], []
        elif self.group == "expression":
            return [], [")"]
        else:
            return [], []
