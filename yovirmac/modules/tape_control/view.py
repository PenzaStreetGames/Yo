from yovirmac.modules.constants import *
from yovirmac.modules.segment_control import find, show


def tape():
    segment = 0
    while segment < len(memory):
        seg_type = find.attribute(segment, "type")
        seg_end = find.attribute(segment, "segment_end")
        if seg_end == 0:
            break
        print(f"{segment} - {seg_end - 1}\t{seg_end - segment}\t\t"
              f"{seg_end - segment - header_length}\t\t{seg_types[seg_type]}")
        segment = seg_end


def data_segment():
    seg_num = find.attribute(seg_links["system"], "first_data_segment")
    number = 1
    while seg_num != 0:
        print(f"Segment #{number}:")
        show.segment_body(seg_num)
        next_num = find.attribute(seg_num, "next_segment")
        seg_num = next_num
        number += 1


def list_segment(num):
    number = 1
    while num != 0:
        print(f"Segment #{number}:", end=" ")
        next_num = find.attribute(num, "next_segment")
        last = True if next_num == 0 else False
        show.list_segment(num, last=last)
        num = next_num
        number += 1


def string_segment(num):
    number = 1
    while num != 0:
        print(f"Segment #{number}:", end=" ")
        next_num = find.attribute(num, "next_segment")
        last = True if next_num == 0 else False
        show.string_segment(num, last=last)
        num = next_num
        number += 1


def namespace(num):
    number = 1
    while num != 0:
        print(f"Segment #{number}:", end=" ")
        next_num = find.attribute(num, "next_segment")
        last = True if next_num == 0 else False
        show.namespace(num, last=last)
        num = next_num
        number += 1
