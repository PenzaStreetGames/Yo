from yovirmac.modules.constants import *
from yovirmac.modules.types_control import write, read
from yovirmac.modules.errors import *
from yovirmac.modules.segment_control.functions import *


def attribute(num, name, value):
    index, kind = find_attribute(num, name)
    write.entity(index, kind, value)
