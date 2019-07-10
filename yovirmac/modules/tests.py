from yovirmac.modules.constants import *
from yovirmac.modules.errors import *
from yovirmac.modules.types_control import write, display, shift, read
from yovirmac.modules.segment_control import init, change, find, show, put, take
from yovirmac.modules.tape_control import add, view, setting, extend
from yovirmac.modules.segment_control.functions import *
import random


def cell_overflow_write():
    """Проверка на переполнение путём записи больших значений"""
    value = 1
    for i in range(capacity + 4):
        write.cell(0, value)
        display.cell(0)
        value <<= 1
        value += 1


def cell_overflow_shift():
    """Проверка на переполнение путём битового сдига влево"""
    write.cell(0, 1)
    for i in range(capacity + 4):
        display.cell(0)
        shift.left(0, 1)
        write.bit(0, 0, 1)


def bit_writing():
    """Проверка на запись бита в ячейку"""
    write.clean(0)
    for i in range(capacity + 4):
        write.bit(0, i, 1)
        display.cell(0)
        write.bit(0, i, 0)


def number_writing():
    """Проверка на запись числа в ячейку"""
    write.clean(0)
    for i in range(20):
        number = random.randint(0, 2 ** 32 - 1)
        print(number)
        write.number(0, number)
        display.cell(0)


def type_writing():
    """Проверка на запись типа в ячеку"""
    for kind in types:
        write.kind(0, type)
        print(read.kind(0))
        display.cell(0)


def logic_writing():
    """Проверка на запись логических величин"""
    values = [0, 1, 2]
    for value in values:
        write.logic(0, value)
        print(value, read.logic(0))


def string_writing():
    """Проверка на запись введённой строки"""
    value = input()
    write.string(0, value)
    for i in range(len(value) + 1):
        print(read.cell(i), read.char(i))
    print(read.string(0))


def command_writing():
    """Проверка на запись команды"""
    for i in range(0, len(commands) + 1):
        try:
            write.command(0, i)
            display.command(0)
        except LowerCommandError as error:
            print(error)
    print()
    for abbrev in commands_abbreviation:
        write.command(0, abbrev)
        display.command(0)
    try:
        write.command(0, "no_command")
        display.command(0)
    except LowerCommandError as error:
        print(error)


def entity_writing():
    """Проверка на запись объектов"""
    entities = [
        [0, "none", None],
        [0, "link", 1000],
        [0, "command", 15],
        [0, "logic", 1],
        [0, "number", 255],
        [0, "string", "something"]
    ]
    for entity in entities:
        write.entity(*entity)
        display.cell(0)
        display.cell(1)
        display.entity(0)


def header_part_writing():
    """Проверка на запись части заголовка"""
    for header_type in seg_header.keys():
        write.header_part(0, header_type, {})
        display.header_part(0, header_type)
        for i in range(header_part_length):
            display.cell(i)
            write.clean(i)
        print()


def header_writing():
    """Проверка на запись заголовка"""
    for header_type in seg_header.keys():
        if header_type == "basic":
            continue
        write.header(0, {"type": seg_types.index(header_type)}, {})
        display.header(0)
        print()


def attribute_writing():
    """Проверка на изменение атрибута"""
    add.system_area()
    display.segment(0)
    show.attribute(0, "segment_end")
    show.attribute(0, "memory_stack")
    print()
    change.attribute(0, "segment_end", 64)
    display.segment(0)
    show.attribute(0, "segment_end")
    print()
    change.attribute(0, "memory_stack", 32)
    display.segment(0)
    show.attribute(0, "memory_stack")
    print()


def stack_writing():
    """Проверка на запись стеков"""
    add.system_area()
    add.memory_stack()
    add.call_stack()
    view.tape()


def dictionary_item_writing():
    """Проверка на запись элемента списка"""
    args = [128, 64, 256]
    write.entity(0, "dictionary_item", args)
    display.entity(0)
    change.dictionary_item_part(0, "key", 48)
    display.entity(0)


def data_segment_writing():
    """Проверка на запись сегмента данных"""
    add.system_area()
    add.memory_stack()
    add.call_stack()
    add.data_segment()
    view.tape()


def program_writing():
    """Проверка на запись программы"""
    add.system_area()
    add.memory_stack()
    add.call_stack()
    add.data_segment()
    add.program("program.yovc")
    view.tape()
    program = find.attribute(seg_links["system"], "main_program")
    show.attribute(seg_links["system"], "target_cell")
    show.program_code(program)


def array_writing():
    """Проверка на запись массива"""
    write.entity(0, "array", [5, 10, 15, 20, 25])
    display.entity(0)


def command_with_args_writing():
    """Проверка на запись команды с аргументами"""
    write.command_with_args(0, "Crt", [{"type": "array", "value": [5, 10, 20]}])
    display.command_with_args(0)
    write.command_with_args(0, "Fnd", [{"type": "string", "value": "line"}])
    display.command_with_args(0)
    write.command_with_args(0, "Add", [{"type": "link", "value": 16},
                                       {"type": "link", "value": 22}])
    display.command_with_args(0)


def list_segment_writing():
    """Проверка на запись сегмента списка"""
    setting.initialisation("program.yovc")
    add.list_segment()
    view.tape()


def segment_extending():
    """Проверка на расширение сегментов"""
    segment_nums = setting.initialisation("program.yovc")
    list_num = add.list_segment()
    namespace_num = find.attribute(seg_links["system"], "target_namespace")
    data_num = find.attribute(seg_links["system"], "first_data_segment")
    extend.data_segment(data_num)
    extend.namespace(namespace_num)
    extend.list_segment(list_num)
    view.tape()


def stack_taking_putting():
    """Проверка на заполнение и опустошение стека"""
    real_memory_stack_size = minimal_data_length["memory_stack"]
    minimal_data_length["memory_stack"] = 8
    setting.initialisation("program.yovc")
    num = find.attribute(seg_links["system"], "memory_stack")
    data = [5, 10, 15, 20, 25]
    print("Заполнение:")
    for i in range(len(data)):
        try:
            put.stack(num, "link", data[i])
            show.segment_body(num)
        except LowerCommandError as error:
            print(error)
    print("Извлечение:")
    for i in range(len(data)):
        try:
            obj_type, obj_value = take.stack(num)
            show.segment_body(num)
        except LowerCommandError as error:
            print(error)
    show.segment_body(num)
    minimal_data_length["memory_stack"] = real_memory_stack_size


def data_segment_putting():
    """Проверка на заполнение сегмента данных"""
    real_data_segment_size = minimal_data_length["data_segment"]
    minimal_data_length["data_segment"] = 4


    minimal_data_length["data_segment"] = real_data_segment_size
