from yovirmac.modules.constants import *
from yovirmac.modules.types_control import write


def system_area():
    base_args = {"type": 0, "length": get_min_size("system")}
    write.segment(0, base_args, {})


def get_min_size(kind):
    return header_length + minimal_data_length[kind]
