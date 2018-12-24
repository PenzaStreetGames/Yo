from constants import types, comands, values


def generate(infile, outfile):
    output = []
    with open(filename, mode="r", encoding="utf-8") as file:
        strings = list(map(lambda string: string.strip(), file.readlines()))
        system = list(map(int, strings[:16]))
        current_cell = system[0]
        top_call_stack = system[1]
        start_call_stack = system[2]
        size_call_stack = system[3]
        top_memory_stack = system[4]
        start_memory_stack = system[5]
        size_memory_stack = system[6]
        start_code_segment = system[7]
        size_code_segment = system[8]
        start_data_segment = system[9]
        top_data_segment = system[10]
        size_data_segment = system[11]
        tape_length = system[12]
        output += system

        for line in strings[16:]:
            res = [""]
            if line in comands:
                res = [types["command"], comands[line]]
            elif line in values:
                res = values[line]
            elif line[1:].isdigit():
                letter = line[0]
                number = int(line[1:])
                if letter == "p":
                    number += start_code_segment
                    res = [types["link"], number]
                elif letter == "c":
                    number += start_data_segment
                    res = [types["link"], number]
                elif letter == "n":
                    res = [types["integer"], number]
                else:
                    print(f"Неизвестное число: {line}")
            elif line == "":
                pass
            else:
                print(f"Неизвестная единица: {line}")
                res = [line]
            output += res

        for i in range(len(output)):
            output[i] = str(output[i])
    with open(outname, mode="w", encoding="utf-8") as file:
        file.write("\n".join(output))


filename = input()
outname = input()
generate(filename, outname)