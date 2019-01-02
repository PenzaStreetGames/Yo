memory = []
size = 32


def Use(number):
    global memory
    memory += [False] * size * number


def Stc(number):
    tape = Sst(2)
    Swr(tape, number)


def Sgt(cell):
    number = 0
    factor = 1
    for i in range(size - 1, -1, -1):
        number += factor * cell[i]
        factor *= 2
    return number


def Sst(number):
    cell = []
    for i in range(size):
        cell.insert(0, number % 2)
        number //= 2
    return cell


def Nop():
    pass


def Get(cell, num):
    num = Sgt(num)
    number = 0
    factor = 1
    for i in range(size * num - 1, -1, -1):
        number += factor * cell[i]
        factor *= 2
    return number


def Set(number, num):
    num = Sgt(num)
    cell = []
    for i in range(num * size):
        cell.insert(0, number % 2)
        number //= 2
    return cell


def Acg(cell, num):
    num = Sgt(num)
    number = 0
    factor = 1
    if cell[0] == False:
        for i in range(num * size - 1, 0, -1):
            number += factor * cell[i]
            factor *= 2
    else:
        for i in range(num * size - 1, 0, -1):
            number += factor * (not cell[i])
            factor *= 2
        number = (number + 1) * (-1)
    return number


def Acs(number, num):
    num = Sgt(num)
    cell = [number < 0]
    if number < 0:
        number = abs(number) - 1
    for i in range(1, num * size):
        cell.insert(1, number % 2)
        number //= 2
    if cell[0] == True:
        for i in range(1, num * size):
            cell[i] = not cell[i]
    return cell


def Rdb(address):
    global memory
    return memory[address]


def Wrb(address, value):
    global memory
    memory[address] = value


def Rdc(cell, num):
    num = Sgt(num)
    array = []
    number = Sgt(cell) * size
    for i in range(num * size):
        array += [Rdb(number + i)]
    return array


def Wrc(cell, value, num):
    num = Sgt(num)
    number = Sgt(cell) * size
    for i in range(num * size):
        Wrb(number + i, value[i])


def Srd(cell):
    array = []
    number = Sgt(cell) * size
    for i in range(size):
        array += [Rdb(number + i)]
    return array


def Nrd(cell, num):
    array = []
    number = (Sgt(cell) + num) * size
    for i in range(size):
        array += [Rdb(number + i)]
    return array


def Swr(cell, value):
    number = Sgt(cell) * size
    for i in range(size):
        Wrb(number + i, value[i])


def Nwr(cell, value, num):
    number = (Sgt(cell) + num) * size
    for i in range(size):
        Wrb(number + i, value[i])


def Rar(begin, address, result):
    beg = Sgt(Nrd(begin, 1))
    # obj = Sgt(Nrd(Srd(beg), 1))
    adr = Sgt(Nrd(Nrd(address, 1), 1))
    # ind = Sgt(Nrd(Srd(adr), 1))
    res = Rdc(Sst(beg + adr + 2), Sst(2))
    Wrc(result, res, Sst(2))


def Raw(begin, address, value):
    beg = Nrd(begin, 1)
    obj = Sgt(Nrd(Srd(beg), 1))
    adr = Nrd(address, 1)
    ind = Sgt(Nrd(Srd(adr), 1))
    Wrc(Sst(obj + ind + 1), value, Sst(2))


def Mov(a, b, num):
    Wrc(a, b, num)


def Chg(a, b, num):
    cell1 = Rdc(a, num)
    cell2 = Rdc(b, num)
    Wrc(a, cell2, num)
    Wrc(b, cell1, num)


def Clr(a, num):
    Wrc(a, Set(0, num), num)


def And(a, b, res, num):
    a = Rdc(a, num)
    b = Rdc(b, num)
    res = Sgt(res) * size
    num = Sgt(num)
    for i in range(num * size):
        if a[i] * b[i] == True:
            Wrb(res + i, True)
        else:
            Wrb(res + i, False)


def Or(a, b, res, num):
    a = Rdc(a, num)
    b = Rdc(b, num)
    res = Sgt(res) * size
    num = Sgt(num)
    for i in range(num * size):
        if a[i] + b[i] != False:
            Wrb(res + i, True)
        else:
            Wrb(res + i, False)


def Xor(a, b, res, num):
    a = Rdc(a, num)
    b = Rdc(b, num)
    res = Sgt(res) * size
    num = Sgt(num)
    for i in range(num * size):
        if a[i] + b[i] == True:
            Wrb(res + i, True)
        else:
            Wrb(res + i, False)


def Not(a, res):
    a = Nrd(Nrd(a, 1), 1)
    res = (Sgt(Nrd(res, 1)) + 1) * size
    num = 1
    for i in range(num * size):
        if a[i] == False:
            Wrb(res + i, True)
        else:
            Wrb(res + i, False)


def Rsh(a, res, num):
    a = Rdc(a, num)
    res = Sgt(res) * size
    num = Sgt(num)
    for i in range(num * size - 1):
        Wrb(res + i + 1, a[i])
    Wrb(res, False)


def Lsh(a, res, num):
    a = Rdc(a, num)
    res = Sgt(res) * size
    num = Sgt(num)
    for i in range(1, num * size):
        Wrb(res + i - 1, a[i])
    Wrb(res + num * size - 1, False)


def Ars(a, res, num):
    Rsh(a, res, num)
    cell = Rdc(res, num)
    temp = Rdc(res, num)
    res = Sgt(res) * size
    Wrb(res, cell[1])


def Als(a, res, num):
    bit = Sgt(res) * size
    sign = Rdb(bit)
    Lsh(a, res, num)
    Wrb(bit, sign)


def Eql(a, b, res):
    type_a = Srd(a)
    type_b = Srd(b)
    if type_a == bintypes["link"]:
        val_a = Rdc(Nrd(a, 1), Sst(2))
    else:
        val_a = Rdc(a, Sst(2))
    if type_b == bintypes["link"]:
        val_b = Rdc(Nrd(b, 1), Sst(2))
    else:
        val_b = Rdc(b, Sst(2))
    cell_res = Nrd(res, 1)
    if val_a == val_b:
        Wrc(cell_res, bintypes["logic"] + Sst(1), Sst(2))
    else:
        Wrc(cell_res, bintypes["logic"] + Sst(0), Sst(2))


def Jmp(address):
    adr = Nrd(address, 1)
    Wrc(system["cell"], adr, Sst(1))


def Jif(condition, address):
    cond = Nrd(condition, 1)
    if cond == binvalues["true"]:
        Jmp(address)


def Elv(a, res, num):
    a = Rdc(a, res)
    num = Sgt(num)
    cell = [False] * num * size + a
    num = Sst(num * 2)
    Wrc(res, cell, num)


def Fal(a, res, num):
    a = Rdc(a, res)
    cell = []
    num = Sgt(num) // 2
    for i in range(num * size, num * size * 2):
        cell += [a[i]]
    num = Sst(num)
    Wrc(res, cell, num)


def Ace(a, res, num):
    a = Rdc(a, res)
    num = Sgt(num)
    cell = [a[0]] * num * size + a
    num = Sst(num * 2)
    Wrc(res, cell, num)


def Acf(a, res, num):
    a = Rdc(a, res)
    cell = [a[0]]
    num = Sgt(num) // 2
    for i in range(num * size + 1, num * size * 2):
        cell += [a[i]]
    num = Sst(num)
    Wrc(res, cell, num)


def Add(a, b, res):
    a = Nrd(Nrd(a, 1), 1)
    b = Nrd(Nrd(b, 1), 1)
    trans = False
    res = (Sgt(Nrd(res, 1)) + 1) * size
    num = 1
    for i in range(num * size - 1, -1, -1):
        bit = res + i
        if a[i] * b[i] == True:
            if trans == True:
                Wrb(bit, True)
            else:
                Wrb(bit, False)
                trans = True
        elif a[i] + b[i] == True:
            if trans == True:
                Wrb(bit, False)
                trans = True
            else:
                Wrb(bit, True)
        else:
            if trans == True:
                Wrb(bit, True)
                trans = False
            else:
                Wrb(bit, False)


def Inc(a, res):
    a = Nrd(Nrd(a, 1), 1)
    trans = False
    res = (Sgt(Nrd(res, 1)) + 1) * size
    num = 1
    last = num * size - 1
    if a[last] == True:
        Wrb(res + last, False)
        trans = True
    else:
        Wrb(res + last, True)
    for i in range(last - 1, -1, -1):
        if trans * a[i] == True:
            Wrb(res + i, False)
        elif trans == True:
            Wrb(res + i, True)
            trans = False
        else:
            Wrb(res + i, a[i])


def Dec(a, res):
    a = Nrd(Nrd(a, 1), 1)
    trans = False
    res = (Sgt(Nrd(res, 1)) + 1) * size
    num = 1
    last = num * size - 1
    for i in range(last, -1, -1):
        if trans * a[i] == True:
            Wrb(res + i, True)
        elif trans + a[i] == True:
            Wrb(res + i, False)
            trans = True
        else:
            Wrb(res + i, True)


def Neg(a, res):
    bit = Sgt(Nrd(Nrd(a, 1), 1)) * size
    sign = Rdb(bit)
    if sign == False:
        Not(a, res)
        Inc(res, res)
    else:
        Dec(a, res)
        Not(res, res)


def Sub(a, b, res):
    num = Sst(1)
    cell = Rdc(b, num)
    Neg(b, b)
    Add(a, b, res)
    Wrc(b, cell, num)


def Grt(a, b, res):
    Sub(b, a, res)
    bit = (Sgt(Nrd(res, 1)) + 1) * size
    bit = Rdb(bit)
    if bit == True:
        Wrc(Nrd(res, 1), bintypes["logic"] + binvalues["true"], Sst(2))
    else:
        Wrc(Nrd(res, 1), bintypes["logic"] + binvalues["false"], Sst(2))


def Les(a, b, res):
    Sub(a, b, res)
    bit = (Sgt(Nrd(res, 1)) + 1) * size
    bit = Rdb(bit)
    if bit == True:
        Wrc(Nrd(res, 1), bintypes["logic"] + binvalues["true"], Sst(2))
    else:
        Wrc(Nrd(res, 1), bintypes["logic"] + binvalues["false"], Sst(2))


def Mul(a, b, res, num):
    cella = Rdc(a, num)
    cellb = Rdc(b, num)
    if cella[0] == True:
        signa = True
        Neg(a, a, num)
    else:
        signa = False
    if cellb[0] == True:
        signb = True
        Neg(b, b, num)
    else:
        signb = False
    cells = Sgt(num)
    for i in range(cells * size - 1, -1, -1):
        if cellb[i] == True:
            Add(a, res, res, num)
        Als(a, a, num)
    if signa + signb == True:
        Neg(res, res, num)
    Wrc(a, cella, num)


def Div(a, b, res, rest, num):
    cella = Rdc(a, num)
    cellb = Rdc(b, num)
    if cella[0] == True:
        signa = True
        Neg(a, a, num)
    else:
        signa = False
    if cellb[0] == False:
        signb = False
        Neg(b, b, num)
        cellb = Rdc(b, num)
    else:
        signb = True
    cells = Sgt(num)
    res = Sgt(res) * size
    Clr(b, num)
    bitb = Sgt(b) * size
    Wrb(bitb, True)
    for i in range(1, cells * size):
        Ars(b, b, num)
        bit = cells * size - i
        Wrb(bitb + 1, cellb[bit])
        Add(a, b, rest, num)
        cell = Rdc(rest, num)
        if cell[0] == False:
            Wrc(a, cell, num)
            Wrb(res + i, True)
        else:
            Wrb(res + i, False)
            # Clr(rest, num)
    cellrest = Rdc(a, num)
    Mov(rest, cellrest, num)
    if signa + signb == True:
        res //= size
        res = Sst(res)
        Neg(res, res, num)
    Wrc(a, cella, num)
    if signb == False:
        Neg(b, b, num)


def Psh(a):
    vertex = system["tp_stc"]
    a = Rdc(a, Sst(2))
    top = Srd(vertex)
    Wrc(top, a, Sst(2))
    cells = 2
    top = Sgt(top)
    top = Sst(top + cells)
    Swr(vertex, top)


def Pop(a):
    vertex = system["tp_stc"]
    cells = 2
    top = Srd(vertex)
    top = Sgt(top)
    top = Sst(top - cells)
    type_a = Srd(top)
    if type_a != bintypes["none"]:
        cell = Rdc(top, Sst(2))
        Wrc(Nrd(a, 1), cell, Sst(2))
        Clr(top, Sst(2))
    Swr(vertex, top)


def Cal(procedure):
    target = system["cell"]
    now = Srd(target)
    now = Sgt(now)
    # address = Sst(now + 4)

    # Psh(address)
    vertex = system["tp_cst"]
    top = Srd(vertex)
    Wrc(top, bintypes["link"] + Sst(now), Sst(2))
    cells = 2
    top = Sgt(top)
    top = Sst(top + cells)
    Swr(vertex, top)

    Jmp(procedure)


def Ret():
    # Pop (cell)
    vertex = system["tp_cst"]
    cells = 2
    top = Srd(vertex)
    top = Sgt(top)
    top = Sst(top - cells)
    cell = Nrd(top, 1)
    Clr(top, Sst(2))
    Swr(vertex, top)

    Swr(system["cell"], cell)


def End():
    Swr(system["cell"], system["cell"])


def Wrt(a, b):
    type_b = Srd(b)
    if type_b == bintypes["link"]:
        Nwr(a, Nrd(b, 1), 1)
    else:
        Nwr(a, b, 1)
    Bit(a, Sst(1))
    Bit(Sst(Sgt(a) + 1), Sst(1))


def Inp(address):
    word = input()
    type_a = Srd(address)
    if type_a != bintypes["link"]:
        for symbol in word:
            symbol = ord(symbol)
            symbol = Sst(symbol)
            Swr(a, symbol)
            a = Sgt(address)
            a = Sst(address + 1)
        end = Sst(0)
        Swr(address, end)


def Inm(address, num):
    number = int(input())
    number = Set(number, num)
    Wrc(address, number, num)


def Inb(address, num):
    bits = input()
    cell = []
    for bit in bits:
        if bit == "1":
            cell += [True]
        elif bit == "0":
            cell += [False]
    Swr(address, cell)


def Chr(address):
    num = Sst(1)
    symbol = Srd(address)
    symbol = Sgt(symbol)
    symbol = chr(symbol)
    print(symbol, end="")


def Wrd(address):
    symbol = Srd(address)
    end = Sst(0)
    while symbol != end:
        Chr(address)
        address = Sgt(address)
        address = Sst(address + 1)
        symbol = Srd(address)


def Num(address):
    number = Nrd(Nrd(address, 1), 1)
    number = Sgt(number)
    print(number)


def Acn(address, num):
    number = Rdc(address, num)
    number = Acg(number, num)
    print(number)


def Bit(address, num):
    cell = Rdc(address, num)
    address = Sgt(address) * size
    num = Sgt(num)
    for i in range(num * size):
        bit = cell[i]
        if bit == True:
            print("1", end="")
        else:
            print("0", end="")
    print()


def Exc():
    address = Srd(system["cell"])
    com = Nrd(address, 1)
    name = ""
    for command in comands.items():
        if command[1] == Sgt(com):
            name = command[0]
            break
    nargs = number_args[name]
    args = []
    for i in range(nargs):
        args += [Sst(Sgt(address) + (i + 1) * 2)]
    func = functions[name]
    Swr(system["cell"], Sst(Sgt(address) + (nargs + 1) * 2))
    print(Sgt(address) - 528, func.__name__, *list(map(lambda arg: Sgt(arg) - 528, map(lambda arg: Nrd(arg, 1), args))))
    func(*args)


from constants import (bintypes, binvalues, system, comands, number_args)
functions = {"end": End, "use": Use, "mov": Mov, "chg": Chg, "clr": Clr,
             "rar": Rar, "raw": Raw, "and": And, "or": Or, "xor": Xor,
             "not": Not, "rsh": Rsh, "lsh": Lsh, "ars": Ars, "als": Als,
             "jmp": Jmp, "jif": Jif, "elv": Elv, "fal": Fal, "ace": Ace,
             "acf": Acf, "neg": Neg, "add": Add, "inc": Inc, "dec": Dec,
             "sub": Sub, "mul": Mul, "div": Div, "psh": Psh, "pop": Pop,
             "cal": Cal, "ret": Ret, "eql": Eql, "grt": Grt, "les": Les,
             "inp": Inp, "inm": Inm, "inb": Inb, "chr": Chr, "wrd": Wrd,
             "num": Num, "bit": Bit, "acn": Acn, "exc": Exc, "nop": Nop,
             "stc": Stc, "wrt": Wrt}


def load_program(filename):
    with open(filename, mode="rb") as file:
        binary = file.read()
        cells = []
        print(len(binary) // 4 + 1)
        for i in range(len(binary) // 4 + 1):
            cells += [binary[size // 8 * i: size // 8 * (i + 1)]]
            print(cells[i])
        binary = list(map(list, cells))
        sys, code = binary[:16 * size], binary[16 * size:]
        tape = Sgt(sys[12 * size: 13 * size])
        Use(tape)
        Wrc(system["cell"], sys, Sst(16))
        Wrc(Sst(Sgt(Srd(system["st_csg"])) + 2), code, Sst(len(code) // size))


def work():
    load_program(input())
    # print_code()
    cell = Srd(system["cell"])
    while cell != system["cell"]:
        # print(Sgt(cell))
        Exc()
        cell = Srd(system["cell"])


def test():
    Use(48)

    Wrc(system["cell"], Sst(4), Sst(1))
    Wrc(Sst(12), bintypes["integer"] + Sst(10), Sst(2))
    Wrc(Sst(14), bintypes["integer"] + Sst(7), Sst(2))
    Wrc(Sst(4), bintypes["command"] + Sst(comands["sub"]), Sst(2))
    Wrc(Sst(6), bintypes["link"] + Sst(12), Sst(2))
    Wrc(Sst(8), bintypes["link"] + Sst(14), Sst(2))
    Wrc(Sst(10), bintypes["link"] + Sst(16), Sst(2))

    Exc()
    Bit(system["cell"], Sst(1))
    Num(Sst(10))


def print_tape():
    for i in range(Sgt(Srd(system["tape"]))):
        print(i, end="\t")
        Bit(Sst(i), Sst(1))


def print_code():
    begin = Sgt(Srd(system["st_csg"]))
    end = begin + Sgt(Srd(system["sz_csg"]))
    for i in range(begin, end, 2):
        type_a = Srd(Sst(i))
        value = Nrd(Sst(i), 1)
        if type_a == bintypes["command"]:
            for comand in comands.items():
                if comand[1] == Sgt(value):
                    print(i - 528, end="\t")
                    print(comand[0], end="\n")
                    break


# test()
work()
