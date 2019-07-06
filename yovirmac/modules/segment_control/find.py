from yovirmac.modules.segment_control.functions import *
from yovirmac.modules.types_control import read


def attribute(num, name):
    index, kind = find_attribute(num, name)
    kind, value = read.entity(index)
    return value
