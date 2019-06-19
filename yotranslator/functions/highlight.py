from yotranslator.modules.constants import *
from copy import deepcopy
import json

tokens = deepcopy(highlight_tokens)


def add_token(yo_object):
    if yo_object.name == "\n":
        return
    tokens[yo_object.color_group] += [
                                        {
                                            "name": yo_object.name,
                                            "row": yo_object.row,
                                            "begin": yo_object.text_begin,
                                            "end": yo_object.text_end
                                        }
                                     ]


def make_hint(filename):
    with open(f"{filename}.yohl", mode="w") as outfile:
        outfile.write(json.dumps(tokens, indent=4))
