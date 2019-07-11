from yovirmac.modules.segment_control import find


def list_segment(num):
    result = []
    while num != 0:
        next_num = find.attribute(num, "next_segment")
        last = True if next_num == 0 else False
        result += find.list_segment(num, last=last)
        num = next_num
    return result


def string_segment(num):
    result = ""
    while num != 0:
        next_num = find.attribute(num, "next_segment")
        last = True if next_num == 0 else False
        result += find.string_segment(num, last=last)
        num = next_num
    return result


def namespace(num):
    result = []
    while num != 0:
        next_num = find.attribute(num, "next_segment")
        last = True if next_num == 0 else False
        result += find.namespace(num, last=last)
        num = next_num
    return result
