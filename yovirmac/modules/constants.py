from json import loads

memory = []
capacity = 32

with open("config.yocfg", "r") as infile:
    config = loads(infile.read())
