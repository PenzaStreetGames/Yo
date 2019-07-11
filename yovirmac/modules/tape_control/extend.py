from yovirmac.modules.constants import *
from yovirmac.modules.tape_control import add
from yovirmac.modules.segment_control import find, change


def data_segment(num):
    new_size = calculate_new_size(num)
    new_num = add.create_segment("data_segment", self_length=new_size)
    attach_with_old_segment(num, new_num)
    change.attribute(seg_links["system"], "last_data_segment", new_num)
    add.empty_data(new_num)
    return new_num


def namespace(num):
    new_size = calculate_new_size(num)
    new_num = add.create_segment("namespace", self_length=new_size)
    attach_with_old_segment(num, new_num)
    add.empty_data(new_num)
    return new_num


def list_segment(num):
    new_size = calculate_new_size(num)
    new_num = add.create_segment("list_segment", self_length=new_size)
    attach_with_old_segment(num, new_num)
    add.empty_data(new_num)
    return new_num


def string_segment(num):
    new_size = calculate_new_size(num)
    new_num = add.create_segment("string_segment", self_length=new_size)
    attach_with_old_segment(num, new_num)
    add.empty_data(new_num)
    return new_num


def calculate_new_size(num):
    previous_size = find.attribute(num, "length") - header_length
    new_size = previous_size * expansion_coefficient
    return new_size


def attach_with_old_segment(num, new_num):
    change.attribute(num, "next_segment", new_num)
    change.attribute(new_num, "previous_segment", num)
