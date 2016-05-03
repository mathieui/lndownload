import os.path
from ebooklib import epub
from .custom_types import BookAttrs

def create_book(attrs: BookAttrs, chapter_list: list):
    book = epub.EpubBook()

    book.set_identifier(attrs.identifier)
    book.set_title(attrs.title)
    book.set_language(attrs.lang)

    book.add_author(attrs.author)

    chapters = []
    for chapter_num, chapter_title, filename in chapter_list:
        chap = epub.EpubHtml(title=chapter_title,
                             file_name='{}-{}.html'.format(attrs.abbrev, chapter_num))
        with open(filename) as fd:
            chap.content = fd.read()
        chapters.append(chap)
    for chapter in chapters:
        book.add_item(chapter)

    # define Table Of Contents
    book.toc = ((epub.Section(attrs.title), chapters),)

    # add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # empty CSS style
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content='')

    # add CSS file
    book.add_item(nav_css)

    # basic spine
    spine = ['nav']
    spine.extend(chapters)
    book.spine = spine

    # write to the file
    epub.write_epub('books/{}.epub'.format(attrs.abbrev), book, {})

