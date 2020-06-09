from yostructer.classes.highlighter import Highlighter


class HtmlHighlighter(Highlighter):

    def __init__(self, document):
        super().__init__(document)
        self.groups = [
            "non_colored",
            "tag",
            "attribute",
            "sign",
            "string",
            "comment",
        ]
        self.styles = {
            "non_colored": {"color": [245, 245, 245]},
            "comment": {"color": [128, 128, 128]},
            "sign": {"color": [255, 207, 64]},
            "string": {"color": [0, 255, 127]},
            "tag": {"color": [242, 221, 198]},
            "attribute": {"color": [253, 234, 168]},
            "error": {"color": [239, 48, 56]}
        }
        self.expressions = {
            "non_colored": r".",
            "comment": r"\<\!\-\-.*?\-\-\>",
            "sign": r"[\<\>\/\=]",
            "string": r"\".*?\"|'.*?'",
            "tag": r"\<.*\>",
            "attribute": r"\S*\=|\S*\,"
        }
        self.styles = self.get_format_types()
