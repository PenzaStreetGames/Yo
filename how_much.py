import os
answer = []


def get_info(folder, nesting):
    global answer
    print(answer)
    structure = {"folders": 0, "files": 0, "strings": 0}
    for obj in os.scandir(folder):
        if obj.is_dir():
            if obj.name.startswith("."):
                continue
            if obj.name == "__pycache__":
                continue
            if obj.name == "force_of_sharps":
                continue
            if obj.name == "TestExample":
                continue
            children_structure = get_info(obj.path, nesting + 1)
            structure["folders"] += 1
            structure["folders"] += children_structure["folders"]
            structure["files"] += children_structure["files"]
            structure["strings"] += children_structure["strings"]
        elif obj.is_file():
            if obj.name.startswith("."):
                continue
            if obj.name == "__init__.py":
                continue
            if obj.name.endswith(".py"):
                structure["files"] += 1
                with open(obj.path, "r", encoding="utf-8") as file:
                    strings = len(file.readlines())
                    structure["strings"] += strings
                answer += ["\t" * (nesting + 1) + f"file {obj.name} {strings} "
                           f"строк"]
    name = folder.split('\\')[-1]
    answer += ["\t" * nesting + f"folder {name} "
               f"{structure['folders']} папок {structure['files']} файлов "
               f"{structure['strings']} строк"]
    return structure


if __name__ == '__main__':
    get_info(os.getcwd(), 0)
    print(*answer[::-1], sep="\n")
