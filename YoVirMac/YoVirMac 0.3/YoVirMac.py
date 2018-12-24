memory = []
size = 32

def Use (number): # Using memory
    global memory
    memory += [False] * number * size

def Nop (): # Empty command
    pass

def Get (cell, num):
    number = 0
    factor = 1
    for i in range((num * size) - 1, -1, -1):
        number = number + cell[i] * factor
        factor = factor * 2
    return number

def Acg (cell, num): # Additional Code Get
    number = 0
    factor = 1
    for i in range((num * size) - 1, 0, -1):
        number = number + cell[i] * factor
        factor = factor * 2
    if cell[0] == True:
        number = number * (-1) - 1
    return number

def Set (number, num):
    cell = []
    power = 2 ** (num * size - 1)
    for i in range(num * size):
        if number >= power:
            cell = cell + [True]
            number = number - power
        else:
            cell = cell + [False]
        power = power // 2
    return cell

def Acs (number, num): # Additional Code Set
    cell = []
    if number >= 0:
        cell = cell + [False]
    else:
        cell = cell + [True]
        number = number * (-1) - 1
    power = 2 ** (num * size - 2)
    for i in range(num * size - 1):
        if number >= power:
            cell = cell + [True]
            number = number - power
        else:
            cell = cell + [False]
        power = power // 2
    if cell[0] == True:
        for i in range(1, num * size):
            if cell[i] == False:
                cell[i] = True
            else:
                cell[i] = False
    return cell

def Fil (cell, now, need): # FILling cell
    array = []
    if now - need >= 0:
        for i in range((now - need) * size, now * size):
            array += [cell[i]]
    else:
        array += [False] * (need - now) + cell
    return array

def Acf (cell, now, need): # Additional Code Fill
    array = []
    sign = cell[0]
    if now - need >= 0:
        array += [sign]
        for i in range((now - need) * size + 1, now * size):
            array += [cell[i]]
    else:
        array += [sign] * (need - now) + cell
    return array

def Lgf (cell, now, need): # LoGical Fill
    array = []
    sign = cell[0]
    if now - need >= 0:
        array += [sign]
        for i in range((now - need) * size - 1, now * size):
            array += [cell[i]]
    else:
        array += [sign] * (need - now) + cell
    return array

def Lgg (a, numa, numb): # LoGical Get
    a = Rdc(a, numa)
    a = Lgf(a, numa, numb)
    return a

def Ace (a, numa, numb): # Additional Code Elevate
    a = Rdc(a, numa)
    a = Acf(a, numa, numb)
    return a

def Rdb (address): # ReaD Bit
    global memory
    return memory[address]

def Wrb (address, value): # WRite Bit
    global memory
    memory[address] = value
    
def Rdc (cell, num): # ReaD Cell
    array = []
    number = Get(cell, 1) * size
    for i in range(num * size):
        array += [Rdb(number + i)]
    return array

def Wrc (cell, value, num): # WRite Cell
    number = Get(cell, 1) * size
    for i in range(num * size):
        Wrb(number + i, value[i])

def Mov (a, b, num): # MOVe value in cell
    Wrc(a, b, num)
    
def Swp (a, b, num): # SWaP
    cell1, cell2 = Rdc(a, num), Rdc(b, num)
    Wrc(a, cell2, num)
    Wrc(b, cell1, num)
    
def Not (a, numa, res, numres): # logical NOT
    a = Lgg(a, numa, numres)
    res = Get(res, 1) * size
    for i in range(numres * size):
        if a[i] == False:
            Wrb(res + i, True)
        else:
            Wrb(res + i, False)

def And (a, numa, b, numb, res, numres): # logical AND
    a = Lgg(a, numa, numres)
    b = Lgg(b, numb, numres)
    res = Get(res, 1) * size
    for i in range(numres * size):
        if a[i] * b[i] == True:
            Wrb(res + i, True)
        else:
            Wrb(res + i, False)

def Or (a, numa, b, numb, res, numres): # logical OR
    a = Lgg(a, numa, numres)
    b = Lgg(b, numb, numres)
    res = Get(res, 1) * size
    for i in range(numres * size):
        if a[i] + b[i] != False:
            Wrb(res + i, True)
        else:
            Wrb(res + i, False)
            
def Xor (a, numa, b, numb, res, numres): # logical XOR
    a = Lgg(a, numa, numres)
    b = Lgg(b, numb, numres)
    res = Get(res, 1) * size
    for i in range(numres * size):
        if a[i] + b[i] == True:
            Wrb(res + i, True)
        else:
            Wrb(res + i, False)
            
def Rsh (a, numa, res, numres): # Right SHift
    a = Lgg(a, numa, numres)
    res = Get(res, 1) * size
    for i in range(numres * size - 1):
        bit = a[i]
        Wrb(res + i + 1, bit)
    Wrb(res, False)

def Lsh (a, numa, res, numres): # Left SHift
    a = Lgg(a, numa, numres)
    res = Get(res, 1) * size
    for i in range(1, numres * size):
        bit = a[i]
        Wrb(res + i - 1, bit)
    Wrb(res + numres - 1, False)

def Als (a, numa, res, numres): # Arithmetic Left Shift
    a = Ace(a, numa, numres)
    res = Get(res, 1) * size
    sign = Rdb(res)
    for i in range(1, numres * size):
        bit = a[i]
        Wrb(res + i - 1, bit)
    Wrb(res + num - 1, sign)
    
def Ars (a, numa, res, numres): # Arithmetic Right Shift
    Rsh(a, numa, res, numres)
    
def Eql (a, numa, b, numb, res, numres): # EQuaLs
    And(a, numa, b, numb, res, numres)
    cell = Rdc(res, numres)
    number = True
    for i in range(numres * size):
        number = number * cell[i]
    value = Set(number, numres)
    Wrc(res, value, numres)

def Jmp (address): # JuMP
    Wrc(Set(0, 1), address, 1)
    
def Jif (cond, a, numa, b, numb, res, numres, address): # Jump IF
    cond = Get(cond, 1)
    if cond == 10:
        Eql(a, numa, b, numb, res, numres)
    # ...Etcetera...
    else:
        Nop()
    res = Get(res, numres)
    if res == True:
        Jmp(address)

def Add (a, numa, b, numb, res, numres): # Add number
    a = Ace(a, numa, numres)
    b = Ace(b, numb, numres)
    trans = False
    res = Get(res, 1) * size
    for i in range(numres * size - 1, -1, -1):
        if a[i] * b[i] == True:
            if trans == True:
                bit = True
            else:
                bit = False
            trans = True
        elif a[i] + b[i] == True:
            if trans == True:
                bit = False
                trans = True
            else:
                bit = True
        else:
            if trans == True:
                bit = True
                trans = False
            else:
                bit = False
        Wrb(res + i, bit)

def Neg (a, numa, res, numres): # NEGative number
    bit = Get(a, 1) * size
    sign = Rdb(bit)
    if sign == False:
        Not(a, numa, res, numres)
        Add(res, numres, Set(2, 1), 1, res, numres) # "-1" in cell 2
    else:
        Add(a, numa, Set(3, 1), 1, res, numres) # "1" in cell 3
        Not(res, numres, res, numres)
        
def Sub (a, numa, b, numb, res, numres): # SUBstraction
    cell = Rdc(b, numb)
    Neg(b, numb, b, numb)
    Add(a, numa, b, numb, res, numres)
    Wrc(b, cell, numb)
    
def Grt (a, numa, b, numb, res, numres): # GReaTer
    Sub(b, numb, a, numa, res, numres)
    bit = Get(res, 1) * size
    sign = Rdb(bit)
    if sign == True:
        value = Set(1, numres)
    else:
        value = Set(0, numres)
    Wrc(res, value, numres)
    
def Les (a, numa, b, numb, res, numres): # LESs
    Sub(a, numa, b, numb, res, numres)
    bit = Get(res, 1) * size
    sign = Rdb(bit)
    if sign == True:
        value = Set(1, numres)
    else:
        value = Set(0, numres)
    Wrc(res, value, numres)

def Mul (a, numa, b, numb, res, numres): # MULtiplication
    cella = Rdc(a, numa)
    cellb = Rdc(b, numb)
    signa = cella[0]
    signb = cellb[0]
    if signa == True:
        Neg(a, numa)
    if signb == True:
        Neg(b, numb)
    bits = Rdc(a, numa)
    for i in range(numa * size - 1, -1, -1):
        if bits[i] == True:
            Add(res, numres, b, numb, res, numres)
        Lsh(b, numb, b, numb)
    if signa + signb == True:
        Neg(res, numres, res, numres)
    Wrc(a, cella, numa)
    Wrc(b, cellb, numb)
    
def Div (a, numa, b, numb, res, numres, rest, numrest): # DIVision
    cella = Rdc(a, numa)
    cellb = Rdc(b, numb)
    signa = cella[0]
    signb = cellb[0]
    if signa == True:
        Neg(a, numa)
    if signb == False:
        Neg(b, numb)
    rank = 1
    Add(a, numa, b, numb, res, numres)
    temp = Rdc(res, numres)
    while temp[0] == False:
        Als(b, numb, b, numb)
        Add(a, numa, b, numb, res, numres)
        temp = Rdc(res, numres)
        rank += 1
    cell = []
    for i in range(rank):
        Ars(b, numb, b, numb)
        Add(a, numa, b, numb, res, numres)
        temp = Rdc(res, numres)
        if temp[0] == False:
            Swp(a, numa, res, numres)
            cell += [True]
        else:
            cell += [False]
    cell = [False] * (size - rank) + cell
    cell = Acf(cell, rank // size + 1, numres)
    Wrc(res, cell, numres)
    if signa + signb == True:
        Neg(res, numres, res, numres)
        
def Inp (address): #INPut
    symbol = input()[0]
    number = Set(ord(symbol), 1)
    Wrc(address, number)
    
def Chr (address, num): # CHaR
    symbol = Rdc(address, 1)
    symbol = Get(symbol, 1)
    symbol = chr(symbol)
    print(symbol, end = "")
    
def Num (address, num): # NUMber
    number = Rdc(address, num)
    number = Get(number, num)
    print(number)
    
def Bit (address, num): # BIT
    number = Get(address, 1) * size
    for i in range(num * size):
        bit = Rdb(number + i)
        if bit == True:
            print("1", end = "")
        else:
            print("0", end = "")
            
def main ():
    Use(10)
    Mov(Set(2, 1), Acs(-1, 1), 1)
    Mov(Set(3, 1), Acs(1, 1), 1)
    Mov(Set(5, 1), Acs(2, 1), 1)
    address = Set(5, 1)
    result = Set(7, 1)
    Mul(address, 1, address, 1, result, 1)
    Num(Set(7, 1), 1)
    
main()