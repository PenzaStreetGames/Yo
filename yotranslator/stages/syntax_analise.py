from yotranslator.modules.errors import *
from yotranslator.modules.constants import *
from yotranslator.classes.yo_object import YoObject
from yotranslator.functions.is_object import is_object


def syntax_analise(yo_object, result, stores):
    """смысловой анализ токена в синтаксическом дереве программы"""
    pre_object = result[-1]
    last_store = stores[-1]
    # обработка закрытия ветвления
    if (last_store.sub_group == "branching" and
            last_store.args[-1].is_close() and
            yo_object.name not in branching_continue_words and
            yo_object.name != "\n"):
        result = last_store.check_close(result)
        result = last_store.set_close(result)
        stores = stores[:-1]
        last_store = stores[-1]
        pre_object = result[-1]
    # обработка вызова индекса
    if yo_object.group == "sub_object":
        if pre_object.args_number == "no":
            parent = pre_object.parent
            child = parent.remove_arg()
            parent.add_arg(yo_object)
            yo_object.add_arg(child)
        elif pre_object.args_number in ["unary", "binary"]:
            if is_object(pre_object):
                child = pre_object.remove_arg()
                pre_object.add_arg(yo_object)
                yo_object.add_arg(child)
            else:
                raise YoSyntaxError(f"Неправильный запрос индекса {pre_object} "
                                    f"{yo_object}")
        elif pre_object.args_number == "many":
            if is_object(pre_object):
                child = pre_object.parent.remove_arg()
                yo_object.add_arg(child)
            else:
                raise YoSyntaxError(f"Неправильный запрос индекса {pre_object} "
                                    f"{yo_object}")
        new_object = YoObject(None, {"group": "expression",
                                     "sub_group": "index_expression",
                                     "name": "["})
        yo_object.add_arg(new_object)
        result[-1] = yo_object
        result += [new_object]
        stores += [new_object]
    # обработка вызова функции
    elif yo_object.group == "call":
        if pre_object.args_number == "no":
            parent = pre_object.parent
            child = parent.remove_arg()
            parent.add_arg(yo_object)
            yo_object.add_arg(child)
        elif pre_object.args_number in ["unary", "binary"]:
            if is_object(pre_object):
                child = pre_object.remove_arg()
                pre_object.add_arg(yo_object)
                yo_object.add_arg(child)
            else:
                raise YoSyntaxError(f"Неправильный вызов функции {pre_object} "
                                    f"{yo_object}")
        elif pre_object.args_number == "many":
            if is_object(pre_object):
                child = pre_object.parent.remove_arg()
                yo_object.add_arg(child)
            else:
                raise YoSyntaxError(f"Неправильный запрос индекса {pre_object} "
                                    f"{yo_object}")
        new_object = YoObject(None, {"group": "expression",
                                     "sub_group": "call_expression",
                                     "name": "("})
        yo_object.add_arg(new_object)
        result[-1] = yo_object
        result += [new_object]
        stores += [new_object]
    # пустые вызовы - тоже вызовы
    elif (pre_object.sub_group == "call_expression"
          and yo_object.name in last_store.points):
        result = pre_object.set_close(result)
        result = result[-1].set_close(result)
        stores = stores[:-1]
    # обработка if
    elif (yo_object.group == "structure_word" and yo_object.name == "if" and
          last_store.group == "program"):
        new_object = YoObject(None, {"group": "expression",
                                     "sub_group": "branching",
                                     "name": "branching"})
        new_object.set_indent(pre_object.inside_indent, inside=True)
        yo_object.set_indent(new_object.indent)
        new_object.add_arg(yo_object)
        last_store.add_arg(new_object)
        result += [new_object, yo_object]
        stores += [new_object, yo_object]
    # обработка elseif и else
    elif (yo_object.group == "structure_word" and
          yo_object.name in branching_continue_words):
        if (last_store.sub_group == "branching" and
                last_store.args[-1].name != "else"):
            last_store.add_arg(yo_object)
            result += [yo_object]
            stores += [yo_object]
        else:
            raise YoSyntaxError("Неправильное использование else и elseif")
    # обработка содержимого структур
    elif (last_store.group == "structure_word" and
          yo_object.group == "program"):
        if last_store.name in argument_words:
            result = last_store.args[-1].check_close(result)
            result = last_store.args[-1].set_close(result)
        last_store.add_arg(yo_object)
        result += [yo_object]
        stores += [yo_object]
    # если в однострочной структуре встречается перенос строки -
    # это отступозависимая структура
    elif (last_store.sub_group == "oneline_program" and yo_object.name == "\n"
          and len(last_store.args) == 0):
        parent = last_store.parent
        new_object = YoObject(None, {"group": "program",
                                     "sub_group": "indent_program",
                                     "name": ":"})
        last_store.parent.remove_arg()
        parent.add_arg(new_object)
        new_object.set_indent(parent.inside_indent)
        # new_object.indent = parent.inside_indent
        result[-1] = new_object
        stores[-1] = new_object
    # если после else идёт if, то это одна конструкция else if
    elif (last_store.group == "structure_word" and pre_object.name == "else"
          and yo_object.name == "if"):
        pre_object.name += " if"
        pre_object.sub_group += " if"
    # переносы строк после открывающейся скобки до первого слова не считаются
    elif (yo_object.name == "\n" and last_store.group == "program" and
          len(last_store.args) == 0):
        pass
    # переносы между условием структуры и телом не считаются
    elif (yo_object.name == "\n" and last_store.group == "structure_word" and
          len(last_store.args) == 1):
        pass
    elif yo_object.name in last_store.commas:
        result = last_store.args[-1].check_close(result)
        # if result[-1] != last_store:
        result = last_store.args[-1].set_close(result)
    elif yo_object.name in last_store.points:
        result = last_store.args[-1].check_close(result)
        result = last_store.args[-1].set_close(result)
        result = last_store.set_close(result)
        stores = stores[:-1]
        if result[-1].group == "sub_object":
            result[-1].close = True
        elif result[-1].group == "call":
            result[-1].close = True
        elif result[-1].group == "structure_word":
            if last_store.sub_group == "scopes_program":
                result = result[-1].set_close(result)
                stores = stores[:-1]
            elif last_store.sub_group == "oneline_program":
                result = result[-1].set_close(result)
                stores = stores[:-1]
    elif yo_object.name in groups["punctuation"]:
        raise YoSyntaxError(f"Недопустимый в данном месте знак пунктуации "
                            f"{yo_object}")
    elif yo_object.group == "indent":
        if last_store.sub_group == "indent_program":
            if len(last_store.args) == 0:
                last_store.set_indent(yo_object.indent, inside=True)
                # last_store.inside_indent = yo_object.indent
            else:
                while yo_object.indent != last_store.inside_indent:
                    if yo_object.indent < last_store.inside_indent:
                        result = last_store.args[-1].check_close(result)
                        result = last_store.args[-1].set_close(result)
                        result = last_store.set_close(result)
                        stores = stores[:-1]
                        if len(result) != 1:
                            result = result[-1].set_close(result)
                            stores = stores[:-1]
                    elif yo_object.indent > last_store.inside_indent:
                        raise YoSyntaxError(f"Неуместный отступ {pre_object}")
                    last_store = stores[-1]
    elif pre_object.args_number == "no":
        if yo_object.args_number == "binary":
            pre_object.parent.remove_arg()
            pre_object.parent.add_arg(yo_object)
            yo_object.add_arg(pre_object)
            result[-1] = yo_object
        else:
            raise YoSyntaxError(f"Неразделённые объекты "
                                f"{pre_object}\n{yo_object}")
    elif pre_object.args_number == "unary":
        if yo_object.args_number == "no":
            if len(pre_object.args) == 0:
                pre_object.add_arg(yo_object)
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object}\n{yo_object}")
        elif yo_object.args_number == "unary":
            if len(pre_object.args) == 0:
                pre_object.add_arg(yo_object)
                result += [yo_object]
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object}\n{yo_object}")
        elif yo_object.args_number == "binary":
            if len(pre_object.args) == 1:
                pre_object = pre_object.parent.remove_arg()
                pre_object.parent.add_arg(yo_object)
                yo_object.add_arg(pre_object)
                result[-1] = yo_object
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object}\n{yo_object}")
        elif yo_object.args_number == "many":
            if len(pre_object.args) == 0:
                pre_object.add_arg(yo_object)
                result += [yo_object]
                stores += [yo_object]
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object}\n{yo_object}")
    elif pre_object.args_number == "binary":
        if yo_object.args_number == "no":
            if len(pre_object.args) == 1:
                pre_object.add_arg(yo_object)
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object}\n{yo_object}")
        elif yo_object.args_number == "unary":
            if len(pre_object.args) == 1:
                pre_object.add_arg(yo_object)
                result += [yo_object]
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object}\n{yo_object}")
        elif yo_object.args_number == "binary":
            if len(pre_object.args) == 2:
                priority = ""
                left = pre_object.priority.copy()
                right = yo_object.priority.copy()
                if left[0] != right[0]:
                    priority = "left" if left[0] >= right[0] else "right"
                else:
                    priority = "left" if left[1] >= right[1] else "right"
                if priority == "left":
                    arg2 = pre_object.remove_arg()
                    yo_object.add_arg(arg2)
                    pre_object.add_arg(yo_object)
                    result += [yo_object]
                elif priority == "right":
                    pre_object.parent.remove_arg()
                    pre_object.parent.add_arg(yo_object)
                    yo_object.add_arg(pre_object)
                    result[-1] = yo_object
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object} {yo_object}")
        elif yo_object.args_number == "many":
            if len(pre_object.args) == 1:
                pre_object.add_arg(yo_object)
                result += [yo_object]
                stores += [yo_object]
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object}\n{yo_object}")
    elif pre_object.args_number == "many":
        if pre_object.close:
            if yo_object.args_number == "binary":
                pre_object.parent.remove_arg()
                pre_object.parent.add_arg(yo_object)
                yo_object.add_arg(pre_object)
                result[-1] = yo_object
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object}\n{yo_object}")
        else:
            if not last_store.close:
                if yo_object.args_number in ["no", "unary"]:
                    pre_object.add_arg(yo_object)
                    result += [yo_object]
                elif yo_object.args_number == "many":
                    pre_object.add_arg(yo_object)
                    result += [yo_object]
                    stores += [yo_object]
                elif yo_object.args_number == "many":
                    raise YoSyntaxError(f"Неразделённые объекты "
                                        f"{pre_object}\n{yo_object}")
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object}\n{yo_object}")
    else:
        raise YoSyntaxError(f"Неизвестный объект {yo_object}")
    return result, stores
