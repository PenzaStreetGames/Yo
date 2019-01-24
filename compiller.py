from pprint import pprint

symbols = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_" \
          "АБВГДЕЁЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзиклмнопрстуфхцчшщъыьэюя"
numbers = "0123456789."
signs = ",+-*/%='()[]|{}:?><"
space = " "
quotes = "'\""
comment = "$"
allowed = symbols + numbers + signs + space + quotes + comment
math_op = ["*", "/", "%", "//", "+", "-"]
logic_op = ["=?", "!=", "==?", "!==", ">", "<", ">=", "<=", "=", "+=", "-=", "*=", "/="]
ops = math_op + logic_op
operations_sorted = [["*", "/", "%", "//"], ["+", "-"], [">", "<", ">=", "<=", "=?", "!="], ["="]]

memory = []


def functions_contain(symbol, string):
    for i in range(len(string)):
        if string[i] == symbol:
            return True
    return False


def functions_insert(object):
    global memory
    memory += [object]
    return len(memory)


def compile_lexer(text):
    quote = False
    tokens = []
    for line in text:
        tokens += [["space", len(line) - len(line.lstrip())]]
        for symbol in line:
            if symbol in allowed:
                if symbol is comment: break
                if symbol in quotes:
                    quote = not quote
                    if quote:
                        tokens += [["str", symbol]]
                    else:
                        tokens[-1][-1] += symbol
                if quote and not symbol in quotes:
                    tokens[-1][1] += symbol
                    continue
                if symbol in symbols:
                    if tokens[-1][0] == "id":
                        tokens[-1][1] += symbol
                    elif tokens[-1][0] == "signs":
                        tokens += [["id", symbol]]
                    else:
                        tokens += [["id", symbol]]

                elif symbol in numbers:
                    if tokens[-1][0] == "id":
                        tokens[-1][1] += symbol
                    elif tokens[-1][0] == "numbers":
                        tokens[-1][1] += symbol
                    elif tokens[-1][0] == "signs":
                        tokens += [["numbers", symbol]]
                    else:
                        tokens += [["numbers", symbol]]
                elif symbol in signs:
                    if tokens[-1][0] == "signs" and tokens[-1][1] + symbol in ops:
                        tokens[-1][1] += symbol
                    else:
                        tokens += [["signs", symbol]]
                elif symbol == space:
                    tokens += [[None, None]]
    tokens = [t for t in tokens if t != [None, None]]
    return tokens


def compile_simple_objects(tokens):

    for t in range(len(tokens)):
        if tokens[t][0] == "numbers":
            if functions_contain(".", tokens[t][1]):
                tokens[t] = ["link", functions_insert(["float", tokens[t][1]])]
            else:
                tokens[t] = ["link", functions_insert(["int", tokens[t][1]])]
    return tokens


def compile_brackets(tokens):
    start, stop = None, None
    for t in range(len(tokens)):
        if t < len(tokens):
            if tokens[t] == ['signs', '(']:
                start = t
            elif tokens[t] == ['signs', ')']:
                if stop is None:
                    stop = t
    # pprint(tokens)
    if start and stop:
        this = tokens[start + 1:stop]
        this = compile_operations(this)
        tokens = tokens[:start] + this + tokens[stop + 1:]
        tokens = compile_brackets(tokens)
    return tokens


def compile_complex_objects(tokens):
    start_pos, end_pos = None, 0
    cut_list, el_list = False, False
    for t in range(len(tokens)):
        if t in range(len(tokens)):
            if start_pos is not None:
                if tokens[t] == ["sign", ":"]:
                    cut_list = True
            if tokens[t] == ['signs', '[']:
                if t - 1 >= 0 and tokens[t - 1][0] == "id" or tokens[t - 1][0] == "link":
                    el_list = True
                start_pos = t
            if tokens[t] == ['signs', ']']:
                end_pos = t
                if cut_list:
                    pass
                if el_list:
                    r = functions_insert(["part", tokens[start_pos - 1], tokens[start_pos + 1:end_pos]])
                    tokens = tokens[:start_pos - 1] + [["link", r]] + tokens[end_pos + 1:]
                else:
                    els = [e for e in tokens[start_pos + 1:end_pos] if e != ["signs", ","]]
                    r = functions_insert(["list", els])
                    tokens = tokens[:start_pos] + [["link", r]] + tokens[end_pos + 1:]

                start_pos, end_pos = None, 0
                cut_list, el_list = False, False

    return tokens


def compile_operations(tokens):
    for op_group in operations_sorted:
        for op in op_group:
            where = []
            for t in range(len(tokens)):
                if t <= len(tokens):
                    if tokens[t][1] == op:
                        where += [t]

            for i in range(len(where)):
                t = where[i] - 2 * i
                tokens = tokens[:t - 1] + [[op, tokens[t - 1], tokens[t + 1]]] + tokens[t + 2:]

    return tokens


def compile_call_operations(tokens):
    for t in range(len(tokens)):
        if t < len(tokens):
            if tokens[t] == ['signs', '(']:
                if tokens[t - 1][0] in ["id", "link"]:
                    end, i = None, t
                    while tokens[i] != ['signs', ')']:
                        i += 1
                    args = [el for el in tokens[t + 1:i] if el != ["signs", ","]]
                    tokens = tokens[:t - 1] + [[tokens[t - 1], args]] + tokens[i + 1:]
    return tokens


def compile_conditions(tokens):
    for t in range(len(tokens)):
        if t < len(tokens):
            if tokens[t] == ['id', 'если']:
                tokens = tokens[:t] + [["cond", tokens[t + 1]]] + tokens[t + 3:]
            if tokens[t] == ['id', 'пока']:
                tokens = tokens[:t] + [["cycle_cond", tokens[t + 1]]] + tokens[t + 3:]
    return tokens


def compile_levels(tokens):
    structures = [[]]
    level = tokens[0][1]
    for t in range(1, len(tokens)):
        if tokens[t][0] == "space":

            if tokens[t][1] > level:
                structures += [[]]
            elif tokens[t][1] < level:
                structures[-2] += [structures[-1]]
                structures.pop()
            level = tokens[t][1]
        else:
            structures[-1] += [tokens[t]]
    return structures


with open("test.yo", encoding="utf8") as file:
    text = file.read().split("\n")
tokens = compile_lexer(text)
tokens = compile_simple_objects(tokens)
tokens = compile_complex_objects(tokens)
tokens = compile_call_operations(tokens)
tokens = compile_brackets(tokens)
tokens = compile_operations(tokens)
tokens = compile_conditions(tokens)
tokens = compile_levels(tokens)
print("Программа:")
pprint(tokens)
print()
print("Дерево условной памяти:")
pprint(memory)
