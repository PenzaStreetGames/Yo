def translate(program):
    return program


if __name__ == '__main__':
    with open(f"{input()}.yotext", "r", encoding="utf-8") as infile:
        result = translate(infile.read())
    print(result)
