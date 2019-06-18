from yotranslator.modules.errors import *
import yotranslator.main as shell

test_list = {
    "equating": {
        "test_1": "ok",
        "test_2": ""
    }
}


for group in test_list.keys():
    print(group)
    for test in test_list[group].keys():
        filename = f"tests/{group}/{test}.yotext"
        try:
            shell.compile_program(filename, main=False)
        except BaseYoError as error:
            print("\t", test, error)
        else:
            print("\t", test, "ok")