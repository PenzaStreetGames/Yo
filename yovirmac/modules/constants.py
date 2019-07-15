from json import loads

capacity = 32
memory = []


def get_full_cell():
    raw_full_cell = 1
    for i in range(capacity):
        raw_full_cell <<= 1
    raw_full_cell -= 1
    return raw_full_cell


def get_full_signed_cell():
    raw_full_cell = 1
    for i in range(capacity - 1):
        raw_full_cell <<= 1
    raw_full_cell -= 1
    return raw_full_cell


full_cell = get_full_cell()
full_signed_cell = get_full_signed_cell()

types = [
    "none",
    "link",
    "command",
    "logic",
    "number",
    "chars",
    "array",
    "dictionary_item",
    "char",
    "list"
    "dictionary",
    "segment"
]
types_length = {
    "none": 2,
    "link": 2,
    "command": 2,
    "logic": 2,
    "number": 2,
    "char": 2,
    "chars": "many",
    "char_list": "many",
    "link_list": "many",
    "array": "many",
    "dictionary_item": 8,
    "list": "many",
    "dictionary": "many",
    "segment": "many",
    "command_with_args": "many"
}
default_values = {
    "none": 0,
    "link": 0,
    "command": 0,
    "logic": 0,
    "number": 0,
    "chars": "",
    "char_list": "",
    "link_list": [],
    "list": None,
    "dictionary": None,
    "dictionary_item": None,
    "segment": None
}
seg_types = [
    "system",
    "call_stack",
    "memory_stack",
    "program",
    "data_segment",
    "list_segment",
    "string_segment",
    "namespace",
    "dictionary_segment",
]
seg_header = {
    "basic":
        [
            "type",
            "data_begin",
            "length",
            "segment_end",
            "last_full_cell",
            "first_empty_cell",
            "previous_segment",
            "next_segment",
            "interrupt",
            "free_cells"
        ],
    "system":
        [
            "main_program",
            "target_cell",
            "target_namespace",
            "call_stack",
            "memory_stack",
            "first_data_segment",
            "last_data_segment",
            "tape_length"
        ],
    "call_stack": [],
    "memory_stack": [],
    "program":
        [
            "namespace",
            "parent"
        ],
    "data_segment": [],
    "list_segment": [],
    "string_segment": [],
    "namespace":
        [
            "program"
        ],
    "dictionary_segment": []
}
seg_header_types = {
    "basic":
        {
            "type": "number",
            "data_begin": "link",
            "length": "number",
            "segment_end": "link",
            "last_full_cell": "link",
            "first_empty_cell": "link",
            "previous_segment": "link",
            "next_segment": "link",
            "interrupt": "logic",
            "full": "logic",
            "free_cells": "number"
        },
    "system":
        {
            "main_program": "link",
            "target_cell": "link",
            "target_namespace": "link",
            "call_stack": "link",
            "memory_stack": "link",
            "first_data_segment": "link",
            "last_data_segment": "link",
            "tape_length": "number"
        },
    "call_stack": {},
    "memory_stack": {},
    "program":
        {
            "namespace": "link",
            "parent": "link"
        },
    "data_segment": {},
    "list_segment": {},
    "string_segment": {},
    "namespace":
        {
            "program": "link"
        },
    "dictionary_segment": {},
}
header_part_length = 32
header_base_part_length = 32
header_special_part = 30
header_length = 64
minimal_data_length = {
            "system": 0,
            "call_stack": 512,  # 512
            "memory_stack": 512,  # 512
            "program": 32,
            "data_segment": 2048,  # 2048
            "list_segment": 2048,
            "string_segment": 64,
            "namespace": 256,
            "dictionary_segment": 2048,
        }
expansion_coefficient = 2
commands = [
    "End",
    "Jump",
    "Jump_if",
    "Create",
    "Find",
    "Equate",
    "Length",
    "Sub_object",
    "Input",
    "Output",
    "Push",
    "Pop",
    "Call",
    "Return",
    "Not",
    "And",
    "Or",
    "Xor",
    "Negative",
    "Add",
    "Increment",
    "Decrement",
    "Subtract",
    "Multiply",
    "Divide",
    "Modulo",
    "Equal",
    "Great",
    "Less",
    "No_operation"
]
commands_abbreviation = [
    "End",
    "Jmp",
    "Jif",
    "Crt",
    "Fnd",
    "Eqt",
    "Len",
    "Sob",
    "Inp",
    "Out",
    "Psh",
    "Pop",
    "Cal",
    "Ret",
    "Not",
    "And",
    "Or",
    "Xor",
    "Neg",
    "Add",
    "Inc",
    "Dec",
    "Sub",
    "Mul",
    "Div",
    "Mod",
    "Eql",
    "Grt",
    "Les",
    "Nop"
]
commands_args_number = {
    "End": 0,
    "Jmp": 1,
    "Jif": 2,
    "Crt": 1,
    "Fnd": 1,
    "Eqt": 2,
    "Len": 1,
    "Sob": 2,
    "Inp": 0,
    "Out": 1,
    "Psh": 1,
    "Pop": 1,
    "Cal": 1,
    "Ret": 0,
    "Not": 1,
    "And": 2,
    "Or":  2,
    "Xor": 2,
    "Neg": 1,
    "Add": 2,
    "Inc": 1,
    "Dec": 1,
    "Sub": 2,
    "Mul": 2,
    "Div": 2,
    "Mod": 2,
    "Eql": 2,
    "Grt": 2,
    "Les": 2,
    "Nop": 0
}
seg_links = {
    "system": 0,
    "memory_stack": header_length,
}
dictionary_item_structure = [
    "dictionary",
    "key",
    "value"
]

with open("config.yocfg", "r") as infile:
    config = loads(infile.read())
