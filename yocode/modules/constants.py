import json

with open("modules/basic.yolp", "r", encoding="utf-8") as infile:
    langpack = json.loads(infile.read())

groups = [
    "non_colored",
    "sign",
    "object",
    "number",
    "logic_value",
    "logic_operation",
    "built_in_function",
    "structure",
    "string",
    "comment"
]

expressions = {
    "non_colored": r".",
    "comment": r"#.*",
    "sign": r"[\(\)\[\]\{\}\=\+\-\*\/\%\<\>\?:;,]",
    "logic_value": r"\b{}\b|",
    "logic_operation": r"\b{}\b|",
    "number": r"\b\d+\b",
    "string": r"\".*?\"|'.*?'",
    "object": r"\b\D\B\w*\b|\b\w\b",
    "built_in_function": r"\b{}\b|",
    "structure": r"\b{}\b|"
}

exprs_words_default = {
    "logic_value": ["true", "false"],
    "logic_operation": ["not", "and", "or", "xor"],
    "built_in_function": ["print", "input", "len"],
    "structure": ["if", "else", "elseif", "while", "break", "continue"],
}

translated_groups = [
    "logic_value",
    "logic_operation",
    "built_in_function",
    "structure"
]

translated_words = {
    "logic_value":
    [
        "true",
        "false",
        "none"
    ],
    "logic_operation":
    [
        "not",
        "and",
        "or",
        "xor"
    ],
    "built_in_function":
    [
        "print",
        "input",
        "len"
    ],
    "structure":
    [
        "if",
        "elseif",
        "else",
        "while",
        "break",
        "continue",
        "pass"
    ]
}

styles = {
    "non_colored":
        {
            "color": [165, 165, 165]
        },
    "comment":
        {
            "color": [128, 128, 128]
        },
    "sign":
        {
            "color": [255, 207, 64]
        },
    "logic_value":
        {
            "color": [255, 177, 24]
        },
    "logic_operation":
        {
            "color": [204, 119, 34]
        },
    "number":
        {
            "color": [166, 202, 240]
        },
    "string":
        {
            "color": [0, 255, 127]
        },
    "object":
        {
            "color": [242, 221, 198]
        },
    "built_in_function":
        {
            "color": [147, 112, 216]
        },
    "structure":
        {
            "color": [253, 94, 83]
        },
    "error":
        {
            "color": [239, 48, 56]
        }
}
