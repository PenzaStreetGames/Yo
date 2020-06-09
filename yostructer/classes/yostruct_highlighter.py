from yostructer.classes.highlighter import Highlighter


class YoStructHighlighter(Highlighter):

    def __init__(self, document):
        super().__init__(document)
        self.groups = [
            "non_colored",
            "tag",
            "pass",
            "attribute",
            "sign",
            "string",
            "raw_string",
            "comment",
        ]
        self.styles = {
            "non_colored": {"color": [245, 245, 245]},
            "comment": {"color": [128, 128, 128]},
            "sign": {"color": [255, 207, 64]},
            "string": {"color": [80, 200, 120]},
            "raw_string": {"color": [102, 153, 204]},
            "tag": {"color": [242, 221, 198]},
            "attribute": {"color": [253, 234, 168]},
            "pass": {"color": [218, 165, 32]},
            "error": {"color": [239, 48, 56]}
        }
        self.expressions = {
            "non_colored": r".",
            "comment": r"#.*",
            "sign": r"[\=\:\{\}\(\)\,]",
            "string": r"\".*?\"|'.*?'",
            "raw_string": r"`.*?`",
            "tag": r".",
            "attribute": r"\w*\=|\w*\,|\w*?\b\)",
            "pass": r"pass"
        }
        self.styles = self.get_format_types()
