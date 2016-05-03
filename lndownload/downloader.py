"""
Download and parse files from novel websites
"""

import logging

from os.path import join, exists
from time import sleep
from typing import Union, List, Tuple

from .custom_types import Filter, TagDesc, Page

import bs4
import requests

from .filters import FILTERS

log = logging.getLogger('downloader')
log.setLevel('DEBUG')

class EndOfChaps(Exception):
    pass

############ Cache-related functions ####################

def write_cache(name: str, number: int, page: Page, folder='cache'):
    "Write the page and next url to the cache"
    with open(join(folder, '{}-{}.html'.format(name, number)), 'w') as fd:
        fd.write(page.contents)
    if page.next is not None:
        with open(join(folder, '.{}-{}-next'.format(name, number)), 'w') as fd:
            fd.write(page.next)

def cached_path(name: str, number: int, folder='cache') -> str:
    return join(folder, '{}-{}.html'.format(name, number))

def cached_url_path(name: str, number: int, folder='cache') -> str:
    return join(folder, '.{}-{}-next'.format(name, number))

def is_cached(name: str, number: int, folder='cache') -> bool:
    "Check if cached data exists"
    return exists(cached_path(name, number, folder))

def is_cached_url(name: str, number: int, folder='cache') -> bool:
    "Check if cached data exists"
    return exists(cached_url_path(name, number, folder))

def next_is_cached(name: str, number: int, folder='cache') -> bool:
    "Check if cached data exists"
    return exists(cached_path(name, number, folder))

def get_cached_url(name: str, number: int, folder='cache') -> str:
    "Get a cached 'next url'"
    file = join(folder, '.{}-{}-next'.format(name, number))
    with open(file, 'r') as fd:
        return fd.read().strip()

def get_cached_data(name: str, number: int, folder='cache') -> str:
    "Get a cached page"
    file = join(folder, '{}-{}.html'.format(name, number))
    with open(file, 'r') as fd:
        return fd.read()

#########################################################

def recursive_find(soup, desc: TagDesc):
    res = soup.find(desc.tag, **(desc.attrs))
    while res and desc.chld:
        desc = desc.chld
        res = res.find(desc.tag, **(desc.attrs))
    return res


def grab_page(url: str) -> str:
    """Download a single page"""
    try:
        response = requests.get(url)
    except Exception:
        raise EndOfChaps("on %s" % url)
    if not response.ok:
        raise EndOfChaps("on %s" % url)
    return response.text

def grab_content(page_text: str, rules: Filter) -> Page:
    """
    Parse a single page
    """
    soup = bs4.BeautifulSoup(page_text, 'lxml')
    res = soup.find(rules.content.tag, **(rules.content.attrs))
    if not res:
        raise EndOfChaps
    next_page = recursive_find(soup, rules.next)
    if not next_page:
        next_page = None
    else:
        try:
            next_page = next_page['href']
        except Exception:
            next_page = None


    for each in rules.exclude:
        remove = res.find_all(each.tag, **(each.attrs))
        for tag in remove:
            tag.extract()

    for each in rules.flatten:
        flatten = soup.find_all(each.tag, **(each.attrs))
        for tag in flatten:
            if tag.text:
                tag.insert_before(tag.text)
            tag.extract()
    text = res.encode_contents().decode('utf-8')
    for each in rules.transform:
        text = each(text)
    return Page(text, next_page)


def grab_pages(name: str, start_at: int, rule_name: str, initial='',
               limit=2, pause: Union[int, float]=0.3) -> List[Tuple[int, str, str]]:
    """
    Download the pages and parse them
    """
    ruleset = FILTERS[rule_name]
    current = initial
    number = start_at
    chapters = [] # type: List[Tuple[int, str, str]]
    for _ in range(limit):
        if is_cached(name, number) and is_cached_url(name, number):
            log.info("Using cache for %s %s", name, number)
            current = get_cached_url(name, number)
            chapters.append((number, 'Chapter {}'.format(number), cached_path(name, number)))
            number += 1
            continue
        elif not current:
            log.error('Empty next chapter')
            break

        try:
            page_text = grab_page(current)
            page = grab_content(page_text, ruleset)
            if len(page.contents) < 2000:
                raise EndOfChaps("Chapter too short")
            log.info("Downloaded %s %s (url: %s)", name, number, current)
        except EndOfChaps:
            log.info('Reached end of chapters at %s (url: %s), too short', number, current)
            break
        if page.next is None and is_cached_url(name, number):
            log.info('No next chapter url found, but in cache')
            page.next = get_cached_url(name, number)
        write_cache(name, number, page)
        chapters.append((number, 'Chapter {}'.format(number), cached_path(name, number)))

        if page.next:
            current = page.next
        else:
            log.info('Reached end of chapters at %s (url: %s)', number, current)
            break
        number += 1
        sleep(pause)

    return chapters
