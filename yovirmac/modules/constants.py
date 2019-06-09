from json import loads

capacity = 32
memory = []

with open("config.yocfg", "r") as infile:
    config = loads(infile.read())
