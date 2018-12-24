memory = []
size = 32


def Use(number):
    global memory
    number = Sgt(number)
    memory += [False] * number * size


def Stc(number):
    tape = Sst(2)
    Swr(tape, number)


def Nop():
    pass


def Sgt(cell):
    number = 0
    factor = 1
    for i in range(size - 1, -1, -1):
        number += factor * cell[i]
        factor *= 2
    return number


def Sst(number):
    cell = []
    power = 2 ** (size - 1)
    for i in range(size):
        if number >= power:
            cell += [True]
            number -= power
        else:
            cell += [False]
        power //= 2
    return cell


def Get(cell, num):
    num = Sgt(num)
    number = 0
    factor = 1
    for i in range(num * size - 1, -1, -1):
        number += factor * cell[i]
        factor *= 2
    return number


def Set(number, num):
    num = Sgt(num)
    cell = []
    power = 2 ** (num * size - 1)
    for i in range(num * size):
        if number >= power:
            cell += [True]
            number -= power
        else:
            cell += [False]
        power //= 2
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
            number += factor * (1 - cell[i])
            factor *= 2
        number = number * (-1) - 1
    return number


def Acs(number, num):
    num = Sgt(num)
    cell = []
    power = 2 ** (num * size - 2)
    if number >= 0:
        cell += [False]
    else:
        number = abs(number) - 1
        cell += [True]
    for i in range(1, num * size):
        if number >= power:
            cell += [True]
            number -= power
        else:
            cell += [False]
        power //= 2
    if cell[0] == True:
        for i in range(1, num * size):
            if cell[i] == True:
                cell[i] = False
            else:
                cell[i] = True
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


def Swr(cell, value):
    number = Sgt(cell) * size
    for i in range(size):
        Wrb(number + i, value[i])


def Rar(begin, address, res, num):  # Relative Address Read
    begin = Sgt(begin)
    address = Sgt(address)
    cell = Sst(begin + address)
    cell = Rdc(cell, num)
    Wrc(res, cell, num)


def Raw(begin, address, value, num):  # Relative Address Write
    begin = Sgt(begin)
    address = Sgt(address)
    cell = Sst(begin + address)
    Wrc(cell, value, num)


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


def Not(a, res, num):
    a = Rdc(a, num)
    res = Sgt(res) * size
    num = Sgt(num)
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


def Eql(a, b, res, num):
    And(a, b, res, num)
    number = True
    cell = Rdc(res, num)
    cells = Sgt(num) * size
    for i in range(cells):
        number *= cell[i]
    if number == True:
        Wrc(res, Set(1, num), num)
    else:
        Wrc(res, Set(0, num), num)


def Jmp(address):
    Wrc(Sst(1), address, Sst(1))


def Jif(cond, a, b, res, address, num):
    cond = Sgt(cond)
    if cond == 10:
        Eql(a, b, res, num)
    else:
        Nop()
    res = Get(res, num)
    if res == True:
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


def Add(a, b, res, num):
    a = Rdc(a, num)
    b = Rdc(b, num)
    trans = False
    res = Sgt(res) * size
    num = Sgt(num)
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


def Inc(a, res, num):
    a = Rdc(a, num)
    trans = False
    res = Sgt(res) * size
    num = Sgt(num)
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


def Dec(a, res, num):
    a = Rdc(a, num)
    trans = False
    res = Sgt(res) * size
    num = Sgt(num)
    last = num * size - 1
    for i in range(last, -1, -1):
        if trans * a[i] == True:
            Wrb(res + i, True)
        elif trans + a[i] == True:
            Wrb(res + i, False)
            trans = True
        else:
            Wrb(res + i, True)


def Neg(a, res, num):
    bit = Sgt(a) * size
    sign = Rdb(bit)
    if sign == False:
        Not(a, res, num)
        Inc(res, res, num)
    else:
        Dec(a, res, num)
        Not(res, res, num)


def Sub(a, b, res, num):
    cell = Rdc(b, num)
    Neg(b, b, num)
    Add(a, b, res, num)
    Wrc(b, cell, num)


def Grt(a, b, res, num):
    Sub(b, a, res, num)
    bit = Sgt(res) * size
    bit = Wrb(bit)
    if bit == True:
        Wrc(res, Set(1, num), num)
    else:
        Wrc(res, Set(0, num), num)


def Les(a, b, res, num):
    Sub(a, b, res, num)
    bit = Sgt(res) * size
    bit = Wrb(bit)
    if bit == True:
        Wrc(res, Set(1, num), num)
    else:
        Wrc(res, Set(0, num), num)


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


def Psh(a, num):
    vertex = Sst(1)
    a = Rdc(a, num)
    cells = Sgt(num)
    top = Srd(vertex)
    top = Sgt(top)
    top = Sst(top + cells)
    Wrc(top, a, num)
    Swr(vertex, top)


def Pop(a, num):
    vertex = Sst(1)
    cells = Sgt(num)
    top = Srd(vertex)
    top = Sgt(top)
    top = Sst(top - cells)
    cell = Rdc(top, num)
    Wrc(a, cell, num)
    Swr(vertex, top)


def Cal(procedure):
    num = Sst(1)
    target = Sst(0)
    now = Rdc(target, num)
    now = Sgt(now)
    address = Sst(now + 1)
    Psh(address, num)
    Jmp(procedure)


def Ret():
    num = Sst(1)
    target = Sst(0)
    Pop(target, num)


def End():
    Wrc(Sst(1), Sst(0), Sst(1))


def Inp(address):
    word = input()
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


def Num(address, num):
    number = Rdc(address, num)
    number = Get(number, num)
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
    address = Sst(0)
    command = Srd(address)
    code = Sgt(command)
    number = Sgt(address)
    if code == 0:
        End()
        return
    elif code == 1:
        a = Sst(number + 1)
        cella = Srd(a)
        Use(cella)
        number += 2
    elif code == 2:
        one = Sst(1)
        a = Sst(number + 1)
        num = Sst(number + 2)
        num = Srd(num)
        b = Sst(number + 3)
        b = Rdc(b, num)
        Mov(a, b, num)
        cells = Sst()
        number += 4
    elif code == 3:
        a = Sst(number + 1)
        b = Sst(number + 2)
        num = Sst(number + 3)
        num = Srd(num)
        Chg(a, b, num)
        number += 4
    elif code == 4:
        a = Sst(number + 1)
        num = Sst(number + 2)
        num = Srd(num)
        Clr(a, num)
        number += 3
    elif code == 5:
        begin = Sst(number + 1)
        address = Sst(number + 2)
        res = Sst(number + 3)
        num = Sst(number + 4)
        num = Srd(num)
        Rar(begin, address, res, num)
        number += 5
    elif code == 6:
        begin = Sst(number + 1)
        address = Sst(number + 2)
        num = Sst(number + 3)
        num = Srd(num)
        value = Sst(number + 4)
        value = Rdc(value, num)
        Raw(begin, address, value, num)
        number += 5
    elif code == 7:
        a = Sst(number + 1)
        b = Sst(number + 2)
        res = Sst(number + 3)
        num = Sst(number + 4)
        num = Srd(num)
        And(a, b, res, num)
        number += 5
    elif code == 8:
        a = Sst(number + 1)
        b = Sst(number + 2)
        res = Sst(number + 3)
        num = Sst(number + 4)
        num = Srd(num)
        Or(a, b, res, num)
        number += 5
    elif code == 9:
        a = Sst(number + 1)
        b = Sst(number + 2)
        res = Sst(number + 3)
        num = Sst(number + 4)
        num = Srd(num)
        Xor(a, b, res, num)
        number += 5
    elif code == 10:
        a = Sst(number + 1)
        res = Sst(number + 2)
        num = Sst(number + 3)
        num = Srd(num)
        Not(a, res, num)
        number += 4
    elif code == 11:
        a = Sst(number + 1)
        res = Sst(number + 2)
        num = Sst(number + 3)
        num = Srd(num)
        Rsh(a, res, num)
        number += 4
    elif code == 12:
        a = Sst(number + 1)
        res = Sst(number + 2)
        num = Sst(number + 3)
        num = Srd(num)
        Lsh(a, res, num)
        number += 4
    elif code == 13:
        a = Sst(number + 1)
        res = Sst(number + 2)
        num = Sst(number + 3)
        num = Srd(num)
        Ars(a, res, num)
        number += 4
    elif code == 14:
        a = Sst(number + 1)
        res = Sst(number + 2)
        num = Sst(number + 3)
        num = Srd(num)
        Als(a, res, num)
        number += 4
    elif code == 15:
        address = Sst(number + 1)
        address = Srd(address)
        Jmp(address)
        number += 2
    elif code == 16:
        cond = Sst(number + 1)
        a = Sst(number + 2)
        b = Sst(number + 3)
        res = Sst(number + 4)
        address = Sst(number + 5)
        address = Srd(address)
        num = Sst(number + 6)
        num = Srd(num)
        Jif(cond, a, b, res, address, num)
        number += 7
    elif code == 17:
        a = Sst(number + 1)
        res = Sst(number + 2)
        num = Sst(number + 3)
        num = Srd(num)
        Elv(a, res, num)
        number += 4
    elif code == 18:
        a = Sst(number + 1)
        res = Sst(number + 2)
        num = Sst(number + 3)
        num = Srd(num)
        Fal(a, res, num)
        number += 4
    elif code == 19:
        a = Sst(number + 1)
        res = Sst(number + 2)
        num = Sst(number + 3)
        num = Srd(num)
        Ace(a, res, num)
        number += 4
    elif code == 20:
        a = Sst(number + 1)
        res = Sst(number + 2)
        num = Sst(number + 3)
        num = Srd(num)
        Acf(a, res, num)
        number += 4
    elif code == 21:
        a = Sst(number + 1)
        res = Sst(number + 2)
        num = Sst(number + 3)
        num = Srd(num)
        Neg(a, res, num)
        number += 4
    elif code == 22:
        a = Sst(number + 1)
        b = Sst(number + 2)
        res = Sst(number + 3)
        num = Sst(number + 4)
        num = Srd(num)
        Add(a, b, res, num)
        number += 5
    elif code == 23:
        a = Sst(number + 1)
        res = Sst(number + 2)
        num = Sst(number + 3)
        num = Srd(num)
        Inc(a, res, num)
        number += 4
    elif code == 24:
        a = Sst(number + 1)
        res = Sst(number + 2)
        num = Sst(number + 3)
        num = Srd(num)
        Dec(a, res, num)
        number += 4
    elif code == 25:
        a = Sst(number + 1)
        b = Sst(number + 2)
        res = Sst(number + 3)
        num = Sst(number + 4)
        num = Srd(num)
        Sub(a, b, res, num)
        number += 5
    elif code == 26:
        a = Sst(number + 1)
        b = Sst(number + 2)
        res = Sst(number + 3)
        num = Sst(number + 4)
        num = Srd(num)
        Mul(a, b, res, num)
        number += 5
    elif code == 27:
        a = Sst(number + 1)
        b = Sst(number + 2)
        res = Sst(number + 3)
        rest = Sst(number + 4)
        num = Sst(number + 5)
        num = Srd(num)
        Div(a, b, res, rest, num)
        number += 6
    elif code == 28:
        a = Sst(number + 1)
        num = Sst(number + 2)
        num = Srd(num)
        Psh(a, num)
        number += 3
    elif code == 29:
        a = Sst(number + 1)
        num = Sst(number + 2)
        num = Srd(num)
        Pop(a, num)
        number += 3
    elif code == 30:
        procedure = Sst(number + 1)
        procedure = Srd(procedure)
        Cal(procedure)
        number += 2
    elif code == 31:
        Ret()
        number += 1
    elif code == 32:
        a = Sst(number + 1)
        b = Sst(number + 2)
        res = Sst(number + 3)
        num = Sst(number + 4)
        num = Srd(num)
        Eql(a, b, res, num)
        number += 5
    elif code == 33:
        a = Sst(number + 1)
        b = Sst(number + 2)
        res = Sst(number + 3)
        num = Sst(number + 4)
        num = Srd(num)
        Grt(a, b, res, num)
        number += 5
    elif code == 34:
        a = Sst(number + 1)
        b = Sst(number + 2)
        res = Sst(number + 3)
        num = Sst(number + 4)
        num = Srd(num)
        Les(a, b, res, num)
        number += 5
    elif code == 35:
        address = Sst(number + 1)
        Inp(address)
        number += 2
    elif code == 36:
        address = Sst(number + 1)
        num = Sst(number + 2)
        num = Srd(num)
        Inm(address, num)
        number += 3
    elif code == 37:
        address = Sst(number + 1)
        num = Sst(number + 2)
        num = Srd(num)
        Inb(address, num)
        number += 3
    elif code == 38:
        address = Sst(number + 1)
        Chr(address)
        number += 2
    elif code == 39:
        address = Sst(number + 1)
        num = Sst(number + 2)
        num = Srd(num)
        Num(address, num)
        number += 3
    elif code == 40:
        address = Sst(number + 1)
        num = Sst(number + 2)
        num = Srd(num)
        Acn(address, num)
        number += 3
    elif code == 41:
        address = Sst(number + 1)
        num = Sst(number + 2)
        num = Srd(num)
        Bit(address, num)
        number += 3
    elif code == 42:
        address = Sst(number + 1)
        num = Sst(number + 2)
        num = Srd(num)
        Acn(address, num)
        number += 3
    elif code == 43:
        Exc()
        number += 1
    elif code == 45:
        a = Sst(number + 1)
        cella = Srd(a)
        Stc(cella)
        number += 2
    else:
        Nop()
        number += 1
    number = Sst(number)
    Swr(address, number)


def main():
    # Загрузка файла
    name = input()
    text = open(name).read()
    bits = []
    for bit in text:
        if bit == "1":
            bits += [True]
        elif bit == "0":
            bits += [False]
    tape = []
    for i in range(size):
        tape += bits[i]
    Use(tape)
    stack = []
    for i in range(size, size * 2):
        stack += bits[i]
    Stc(stack)
    stack = Sgt(stack)
    start = stack + 3
    for i in range(size * 2, len(bits)):
        Wrb(start + i, bits[i])
    # Выполнение:
    target = Sst(0)
    cell = Srd(target)
    cell = Sgt(cell)
    while cell != 0:
        Exc()
        cell = Srd(target)
        cell = Sgt(cell)


def test():
    import time
    begin = time.time()
    for i in range(1000000):
        Sst(i)
    end = time.time()
    print(end - begin)


test()
# main()
