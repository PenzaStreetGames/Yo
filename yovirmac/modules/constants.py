from json import loads

capacity = 32
memory = []


with open("config.yocfg", "r") as infile:
    config = loads(infile.read())
    types = config["types"]
    types_length = config["types_length"]
    seg_types = config["seg_types"]
    seg_header = config["seg_header"]
    seg_header_types = config["seg_header_types"]
    segment_properties = config["segment_properties"]
