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
    "logical",
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
    "non": 0,
    "link": 0,
    "command": 0,
    "logical": 0,
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
            "type": "num",
            "data_begin": "lnk",
            "length": "num",
            "segment_end": "lnk",
            "last_full_cell": "lnk",
            "first_empty_cell": "lnk",
            "previous_segment": "lnk",
            "next_segment": "lnk",
            "interrupt": "log",
            "free_cells": "num"
        },
    "system":
        {
            "main_program": "lnk",
            "target_cell": "lnk",
            "target_namespace": "lnk",
            "call_stack": "lnk",
            "memory_stack": "lnk",
            "first_data_segment": "lnk",
            "last_data_segment": "lnk",
            "tape_length": "num"
        },
    "call_stack": {},
    "memory_stack": {},
    "program":
        {
            "namespace": "lnk",
            "parent": "lnk"
        },
    "data_segment": {},
    "list_segment": {},
    "dictionary_segment": {},
    "namespace":
        {
            "program": "lnk"
        }
}
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
