from yovirmac.modules.constants import *
from yovirmac.modules.segment_control import find


def tape():
    segment = 0
    while segment < len(memory):
        seg_type = find.attribute(segment, "type")
        seg_end = find.attribute(segment, "segment_end")
        if seg_end == 0:
            break
        print(f"{segment} - {seg_end - 1}\t{seg_types[seg_type]}")
        segment = seg_end