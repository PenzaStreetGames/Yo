from yotranslator.classes.binary.binary_program import BinaryProgram


def get_bytes(tape):
    byte_array = []
    while tape:
        segment = tape[:8]
        tape = tape[8:]
        byte = list(map(lambda x: x == "1", segment))
        byte_array += [BinaryProgram.dec(byte)]
    byte_array = bytes(byte_array)
    return byte_array
