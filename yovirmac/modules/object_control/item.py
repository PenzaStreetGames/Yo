from yovirmac.modules.tape_control import make, append


def namespace(num, key, value=None):
    key_type, key_value = key
    key_num = make.entity(key_type, key_value)
    if value is not None:
        value_type, value_value = value
        value_num = make.entity(value_type, value_value)
    else:
        value_num = make.entity("none", 0)
    item_num = append.data_segment("dictionary_item", [num, key_num, value_num])
