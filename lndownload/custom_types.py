from typing import Union, List, Callable
from hashlib import md5

class TagDesc:
    __slots__ = ['tag', 'attrs', 'chld']
    def __init__(self, tag: Union[str, bool], attrs: dict, chld: 'TagDesc'=None) -> None:
        """
        tag: a tag selector (either a string with the tag name or a boolean for glob
        attrs: a dict of the attributes of the tag should have
        chld: a child selector, when you need to target more than one tag to query the right element
        """
        self.tag = tag
        self.attrs = attrs
        self.chld = chld

class Filter:
    __slots__ = ['content', 'next', 'exclude', 'flatten', 'transform']
    def __init__(self, content: TagDesc, next_chap: TagDesc, exclude: List[TagDesc],
            flatten:List[TagDesc]=None, transform:List[Callable[[str],str]]=None) -> None:
        """
        content: a selector for the tag that contains the text
        next_chap: a selector for the tag that contains the url
        exclude: a list of selectors to remove from the extracted document
        flatten: a list of selectors to flatten (i.e. remove the tags but keep the text) from the document
        transform: a list of functions to run over the final text
        """
        self.content = content
        self.next = next_chap
        self.exclude = exclude
        if flatten is None:
            flatten = []
        self.flatten = flatten
        if transform is None:
            transform = []
        self.transform = transform


class BookAttrs:
    __slots__ = ['identifier', 'title', 'abbrev', 'lang', 'author']
    def __init__(self, title: str, abbrev: str, lang='en', author='generated') -> None:
        self.identifier = md5(title.encode()).hexdigest()
        self.title = title
        self.abbrev = abbrev
        self.lang = 'en'
        self.author = author

class Page:
    __slots__ = ['next', 'contents']
    def __init__(self, contents: str, next_page: str) -> None:
        self.next = next_page
        self.contents = contents

    def __str__(self) -> str:
        return 'Page(contents={}, next={})'.format(repr(self.contents), repr(self.next))
