from yovirmac.modules.segment_control import init
from yovirmac.modules.tape_control import add


def initialisation(program_path):
    add.system_area()
    add.memory_stack()
    add.call_stack()
    add.data_segment()
    add.program(program_path)
