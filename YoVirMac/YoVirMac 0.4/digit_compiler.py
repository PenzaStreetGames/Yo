def set(num):
    res = ""
    while num > 1:
        sign = num % 2
        res = str(sign) + res
        num //= 2
    res = str(num) + res
    return res


def rjust(num):
    return num.rjust(32, "0")


def generate(infile, outfile):
    with open(filename, mode="r", encoding="utf-8") as file:
        strings = list(map(lambda string: string.strip(), file.readlines()))
        output = []
        for line in strings:
            if line != "":
                output += [rjust(set(int(line)))]
            else:
                output += [""]

        for i in range(len(output)):
            output[i] = str(output[i])

    with open(outname, mode="w", encoding="utf-8") as file:
        file.write("\n".join(output))


filename = input()
outname = input()
generate(filename, outname)