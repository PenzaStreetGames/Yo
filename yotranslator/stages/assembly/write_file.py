from yotranslator.classes.binary.binary_program import BinaryProgram


def write_file(filename, tape):
    """запись результата в файл .yovc"""
    byte_array = []
    while tape:
        segment = tape[:8]
        tape = tape[8:]
        byte = list(map(lambda x: x == "1", segment))
        byte_array += [BinaryProgram.dec(byte)]
    byte_array = bytes(byte_array)
    with open(f"{filename}.yovc", "wb") as file:
        file.write(byte_array)
    return byte_array
