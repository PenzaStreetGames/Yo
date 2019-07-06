from yovirmac.modules.types_control import display
from yovirmac.modules.segment_control.functions import *


def attribute(num, name):
    index, kind = find_attribute(num, name)
    display.entity(index)
