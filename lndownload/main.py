#!/usr/bin/env python
# -*- coding: utf-8 -*-


from argparse import ArgumentParser
import configparser
import textwrap
import logging
import sys
logging.basicConfig()
log = logging.getLogger('main')
log.setLevel('INFO')

from .builder import create_book
from .custom_types import BookAttrs
from .downloader import grab_pages

def parse_args():
    parser = ArgumentParser('ln_download', description=textwrap.dedent(
        """
        Fetch light novels and generate epubs based on a config file and manual
        filters. An example config file and filters is provided.
        """))
    parser.add_argument('-c', '--config', dest="config_file", default='books.ini',
                        help="The config file to use")
    parser.add_argument('book', metavar='book', type=str, nargs='*',
                        help="Books to download/update")
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    parser = configparser.ConfigParser()
    parser.read(args.config_file)
    if not args.book:
        for book in parser.sections():
            if not parser.get(book, 'auto', fallback=True):
                continue
            attrs = BookAttrs(parser.get(book, 'title'), book,
                              parser.get(book, 'lang', fallback='en'),
                              parser.get(book, 'author', fallback=''))
            log.info('='* 30 + 'Downloading {}'.format(repr(attrs)) + '='*30 )
            chapters = grab_pages(book, 1, parser.get(book, 'filter'),
                                  initial=parser.get(book, 'url'),
                                  limit=parser.get(book, 'limit', fallback=2000),
                                  pause=parser.getint(book, 'pause', fallback=1))

            create_book(attrs, chapters)
    else:
        for book in args.book:
            attrs = BookAttrs(parser.get(book, 'title'), book,
                              parser.get(book, 'lang', fallback='en'),
                              parser.get(book, 'author', fallback=''))
            log.info('='* 30 + 'Downloading {}'.format(repr(attrs)) + '='*30 )
            chapters = grab_pages(book, 1, parser.get(book, 'filter'),
                                  initial=parser.get(book, 'url'),
                                  limit=parser.get(book, 'limit', fallback=2000),
                                  pause=parser.getint(book, 'pause', fallback=1))

            create_book(attrs, chapters)



if __name__ == "__main__":
    main()

