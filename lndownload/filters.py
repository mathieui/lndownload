from .custom_types import TagDesc, Filter
from typing import Mapping

import re

def do_stuff(input):
    lines = input.splitlines()
    new_lines = []
    for line in lines:
        if line.strip():
            new_lines.append('<p>' + line + '</p>')
    return '\n'.join(new_lines)

_example = Filter(
    content=TagDesc('div', {'class_': 'chapter-body'}),
    next_chap=TagDesc('li', {'class_': 'next'}, TagDesc('a', {})),
    exclude=[
        TagDesc('a', {}),
        TagDesc(True, {'class_': 'sharedaddy'}),
        TagDesc('hr', {})
    ],
    flatten=[
        TagDesc('div', {}),
    ],
    transform=[do_stuff]
)

FILTERS = {
    'example': _example,
} # type: Mapping[str, Filter]


