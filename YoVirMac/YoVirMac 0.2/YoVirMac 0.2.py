memory = []
size = 32

def Use (number):
    global memory
    number = Sgt(number)
    memory += [False] * number * size

def Nop ():
    pass

def Sgt (cell):
    number = 0
    factor = 1
    for i in range(size - 1, -1, -1):
        number += factor * cell[i]
        factor *= 2
    return number

def Sst (number):
    cell = []
    power = 2 ** (size - 1)
    for i in range(size):
        if number >= power:
            number -= power
            cell += [True]
        else:
            cell += [False]
        power /= 2
    return cell

def Get (cell, num):
    cells = Sgt(num)
    number = 0
    factor = 1
    for i in range(cells * size - 1, -1, -1):
        number += factor * cell[i]
        factor *= 2
    return number

def Set (number, num):
    cells = Sgt(num)
    cell = []
    power = 2 ** (cells * size)
    for i in range(cells * size):
        power = power // 2
        if number >= power:
            number -= power
            cell += [True]
        else:
            cell += [False]
    return cell

def Acg (cell, num):
    cells = Sgt(num)
    number = 0
    factor = 1
    if cell[0] == False:
        for i in range(cells * size - 1, -1, -1):
            number += factor * cell[i]
            factor *= 2
    else:
        for i in range(cells * size - 1, -1, -1):
            number += factor * (1 - cell[i])
            factor *= 2
        number = number * (-1) - 1
    return number

def Acs (number, num):
    cells = Sgt(num)
    cell = []
    power = 2 ** (cells * size - 1)
    if number >= 0:
        cell = [False]
    else:
        number = abs(number) - 1
        cell = [True]
    for i in range(1, cells * size):
        power = power // 2
        if number >= power:
            number -= power
            cell += [True]
        else:
            cell += [False]
    if cell[0] == True:
        for i in range(1, cells * size):
            if cell[i] == True:
                cell[i] = False
            else:
                cell[i] = True
    return cell

def Rdb (address):
    global memory
    return memory[address]

def Wrb (address, value):
    global memory
    memory[address] = value

def Rdc (cell, num):
    global memory
    num = Srd(num)
    cells = Sgt(num)
    array = []
    number = Sgt(cell) * size
    for i in range(cells * size):
        array += [Rdb(number + i)]
    return array

def Srd (cell):
    global memory
    array = []
    number = Sgt(cell) * size
    for i in range(size):
        array += [Rdb(number + i)]
    return array

def Wrc (cell, value, num):
    global memory
    num = Srd(num)
    cells = Sgt(num)
    number = Sgt(cell) * size
    for i in range(cells * size):
        Wrb(number + i, value[i])
        
def Swr (cell, value):
    global memory
    number = Sgt(cell) * size
    for i in range(size):
        Wrb(number + i, value[i])
        
def Mov (a, b, num):
    Wrc(a, b, num)
    
def Mvc (a, b):
    Swr(a, b)
    
def Chg (a, b, num):
    cell1 = Rdc(a, num)
    cell2 = Rdc(b, num)
    Wrc(a, cell2, num)
    Wrc(b, cell1, num)

def And (a, b, res, num):
    a = Rdc(a, num)
    b = Rdc(b, num)
    res = Sgt(res) * size
    cells = Srd(num)
    cells = Sgt(cells)
    for i in range(cells * size):
        if a[i] * b[i] == True:
            Wrb(res + i, True)
        else:
            Wrb(res + i, False)
        
def Or (a, b, res, num):
    a = Rdc(a, num)
    b = Rdc(b, num)
    res = Sgt(res) * size
    num = Sgt(num)
    for i in range(num * size):
        if a[i] + b[i] != False:
            Wrb(res + i, True)
        else:
            Wrb(res + i, False)

def Xor (a, b, res, num):
    a = Rdc(a, num)
    b = Rdc(b, num)
    res = Sgt(res) * size
    num = Sgt(num)
    for i in range(num * size):
        if a[i] + b[i] == True:
            Wrb(res + i, True)
        else:
            Wrb(res + i, False)
            
def Not (a, res, num):
    a = Rdc(a, num)
    res = Sgt(res) * size
    num = Sgt(num)
    for i in range(num * size):
        if a[i] == True:
            Wrb(res + i, False)
        else:
            Wrb(res + i, True)
            
def Rsh (a, res, num):
    a = Rdc(a, num)
    res = Sgt(res) * size
    num = Sgt(num)
    for i in range(num * size - 1):
        bit = a[i]
        Wrb(res + i + 1, bit)
    Wrb(res, False)
    
def Lsh (a, res, num):
    a = Rdc(a, num)
    res = Sgt(res) * size
    num = Sgt(num)
    for i in range(1, num * size):
        bit = a[i]
        Wrb(res + i - 1, bit)
    Wrb(res + num * size - 1, False)
    
def Ars (a, res, num):
    a = Rdc(a, num)
    sign = a[0]
    res = Sgt(res) * size
    for i in range(num * size - 1):
        bit = a[i]
        Wrb(res + i + 1, bit)
    Wrb(res, sign)
    
def Als (a, res, num):
    Lsh(a, res, num)
    
def Eql (a, b, res, num):
    And(a, b, res, num)
    number, bits = True, Rdc(res)
    num = num * size
    for i in range(num):
        number *= bits[i]
    num = num // size 
    if number == True:
        Wrc(res, Set(1, num), num)
    else:
        Wrc(res, Set(0, num), num)
    
def Jmp (address):
    Wrc([False] * size, address, 1)
    
def Jif (cond, a, b, res, num, address):
    cond = Get(cond, 1)
    if cond == 10:
        Eql(a, b, res, num)
    else:
        Nop()
    res = Get(res, num)
    if res == 1:
        Jmp(address)

def Inp (address):
    symbol = input()[0]
    number = Set(ord(symbol))
    Wrc(address, number)
    
def Chr (address, num):
    symbol = Rdc(address, 1)
    symbol = Get(symbol, 1)
    symbol = chr(symbol)
    print(symbol, end = "")
    
def Num (address, num):
    number = Rdc(address, num)
    number = Get(number, num)
    print(number)
    
def Acn (address, num):
    number = Rdc(address, num)
    number = Acg(number, num)
    print(address)
    
def Bit (address, num):
    number = Sgt(address) * size
    cells = Srd(num)
    cells = Sgt(cells)
    for i in range(cells * size):
        bit = Rdb(number + i)
        if bit == True:
            print("1", end = "")
        else:
            print("0", end = "")
    print()
    
def Elv (a, res, num):
    a = Rdc(a, num)
    cell = [False] * num * size + a
    Wrc(res, cell, num * 2)
    
def Fal (a, res, num):
    a = Rdc(a, num)
    cell = []
    for i in range(num * size // 2, num * size):
        cell += [a[i]]
    Wrc(res, cell, num // 2)

def Ace (a, res, num):
    a = Rdc(a, num)
    sign = a[0]
    cell = [sign] * num * size + a
    Wrc(res, cell, num * 2)
    
def Acf (a, res, num):
    a = Rdc(a, num)
    sign = a[0]
    cell = [sign]
    for i in range(num * size // 2 + 1, num * size):
        cell += [a[i]]
    Wrc(res, cell, num // 2)
    
def Add (a, b, res, num):
    a = Rdc(a, num) 
    b = Rdc(b, num) 
    trans = False
    res = Get(res, 1) * size
    for i in range(num * size - 1, -1, -1):
        if a[i] * b[i] == True:
            if trans == True:
                Wrb(res + i, True)
            else:
                Wrb(res + i, False)
            trans = True
        elif a[i] + b[i] == True:
            if trans == True:
                Wrb(res + i, False)
                trans = True
            else:
                Wrb(res + i, True)
        else:
            if trans == True:
                Wrb(res + i, True)
                trans = False
            else:
                Wrb(res + i, False)
                
def Inc (a, res, num):
    a = Rdc(a, num) 
    trans = False
    res = Get(res, 1) * size
    last = num * size - 1
    if a[last] == True:
        trans = True
        Wrb(res + last, False)
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
            
def Dec (a, res, num):
    a = Rdc(a, num)
    trans = False
    res = Get(res, 1) * size
    last = num * size - 1
    for i in range(last, -1, -1):
        if trans * a[i] == True:
            Wrb(res + i, True)
            trans = True
        elif trans + a[i] == True:
            Wrb(res + i, False)
            trans = True
        else:
            Wrb(res + i, True)
            trans = False
                
def Neg (a, res, num):
    bits = Rdc(a, num)
    if bits[0] == False:
        Not(a, res, num)
        Inc(res, res, num)
    else:
        Dec(a, res, num)
        Not(res, res, num)
        
def Sub (a, b, res, num):
    cell = Rdc(b, num)
    Neg(b, b, num)
    Add(a, b, res, num)
    Wrc(b, cell, num)
    
def Grt (a, b, res, num):
    Sub(b, a, res, num)
    bits = Rdc(res, num)
    if bits[0] == True:
        Wrc(res, Set(1, num), num)
    else:
        Wrc(res, Set(0, num), num)
        
def Les (a, b, res, num):
    Sub(a, b, res, num)
    bits = Rdc(res, num)
    if bits[0] == True:
        Wrc(res, Set(1, num), num)
    else:
        Wrc(res, Set(0, num), num)
        
def Mul (a, b, res, num):
    pass
        
def Div (a, b, res, rest, num):
    pass
    
def Exc (address):
    pass
    
def End ():
    Wrc([False] * 32, Set(0, 1))

def main():
    cells = Sst(10)
    Use(cells)
    a = Sst(0)
    b = Sst(1)
    c = Sst(3)
    sz = Sst(2)
    one = Sst(1)
    Swr(sz, one)
    val1 = Set(42, one)
    Mov(a, val1, sz)
    Mov(b, Set(23, one), sz)
    And(a, b, c, sz)
    Bit(a, sz)
    Bit(b, sz)
    Bit(c, sz)

main()