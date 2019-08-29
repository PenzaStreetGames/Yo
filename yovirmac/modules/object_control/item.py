from yovirmac.modules.tape_control import make, append, get
from yovirmac.modules.segment_control import put, find


def write_namespace_name(num, key, value=None):
    key_type, key_value = key
    key_num = make.entity(key_type, key_value)
    if value is not None:
        value_type, value_value = value
        value_num = make.entity(value_type, value_value)
    else:
        value_num = make.entity("none", 0)
    item_num = append.data_segment("dictionary_item", [num, key_num, value_num])
    put.namespace(num, "link_list", [item_num])
    return item_num + 6


def get_dictionary_item(num):
    key_type, key_link = find.dictionary_item_key(num)
    value_type, value_link = find.dictionary_item_value(num)
    key = get.entity(key_link)
    value = get.entity(value_link)
    return key, value
