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
    "logic_value": r"\btrue\b|\bfalse\b",
    "logic_operation": r"\bnot\b|\band\b|\bor\b|\bxor\b",
    "number": r"\b\d+\b",
    "string": r"\".*?\"|'.*?'",
    "object": r"\b\D\B\w*\b|\b\w\b",
    "built_in_function": r"\bprint\b|\binput\b|\blen\b",
    "structure": r"\bif\b|\belseif\b|\belse\b|\bwhile\b|\bbreak\b|\bcontinue\b"
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
