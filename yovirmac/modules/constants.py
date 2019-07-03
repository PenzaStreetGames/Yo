from json import loads

capacity = 32
memory = []


def get_full_cell():
    raw_full_cell = 1
    for i in range(capacity):
        raw_full_cell <<= 1
    raw_full_cell -= 1
    return raw_full_cell


full_cell = get_full_cell()

types = [
    "none",
    "link",
    "command",
    "logic",
    "number",
    "string",
    "list",
    "dictionary",
    "dictionary_item",
    "segment"
]
types_length = {
    "none": 2,
    "link": 2,
    "command": 2,
    "logical": 2,
    "number": 2,
    "string": "many",
    "list": "many",
    "dictionary": "many",
    "dictionary_item": 6,
    "segment": "many"
}
default_values = {
    "none": 0,
    "link": 0,
    "command": 0,
    "logic": 0,
    "number": 0,
    "string": "",
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
    "dictionary_segment",
    "namespace"
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
    "dictionary_segment": [],
    "namespace":
        [
            "program"
        ]
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
    "dictionary_segment": {},
    "namespace":
        {
            "program": "link"
        }
}
header_part_length = 32
header_base_part_length = 32
header_special_part = 30
segment_properties = {
    "minimal_data_length":
        {
            "system": 32,
            "call_stack": 512,
            "memory_stack": 512,
            "program": 32,
            "data_segment": 2048,
            "list_segment": 2048,
            "dictionary_segment": 2048,
            "namespace": 256
        },
    "header_length": 32,
    "header_basic_length": 16,
    "header_special_length": 16,
    "expansion_coefficient": 2
}
commands = [
    "End",
    "Jump",
    "Jump_if",
    "Create",
    "Find",
    "Equate",
    "Input",
    "Output",
    "Push",
    "Pop",
    "Call",
    "Return",
    "Relative_read",
    "Relative_write",
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
    "Inp",
    "Out",
    "Psh",
    "Pop",
    "Cal",
    "Ret",
    "Rar",
    "Raw",
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

with open("config.yocfg", "r") as infile:
    config = loads(infile.read())
