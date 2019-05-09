a = 32
size = 32
cell = ""
for i in range(size):
    print((a >> i) & 1)