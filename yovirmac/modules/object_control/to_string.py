from yovirmac.modules.tape_control import get


def entity(link):
    value_type, value = get.entity(link)
    if value_type == "list_segment":
        return list_segment(value)
    else:
        return str(value)


def list_segment(value):
    result = []
    for link in value:
        obj_type, obj_value = get.entity(link)
        if obj_type == "list_segment":
            obj_value = list_segment(obj_value)
        result += [str(obj_value)]
    return f"[{', '.join(result)}]"