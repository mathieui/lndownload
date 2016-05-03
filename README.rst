ln_download
###########


This is a simple python3 script whose goal is to automate download of light
novels chapters, clean the output, and write them to an epub file.

It relies on filesystem caching to store individual chapters and links to
the next chapters, in order for both to be easily editable, as parsing the
web isn’t an exact science.


You need to create both the `books` and `cache` directories before running
this tool.

Configuration
~~~~~~~~~~~~~

This script uses a configuration file (by default: `books.ini`) containing
the required information for light novel series, with the following format:

::

    [title-abbrev]
    url = http://url-of-the-first-chapter.com/1/ (REQUIRED)
    title = A title (metadata)
    lang = e.g. "en" (metadata)
    author = An author name (metadata)
    auto = a boolean whether the book should be scrapped automatically when running without a parameter
    filter = the name of a filter (defined in filters.py) (REQUIRED)

There can be any number of these sections in the config file.

Filtering
~~~~~~~~~

You have to define filters for the sites you want to scrap, it’s usually
a straightforward process (and most of those sites use wordpress anyway,
so the structure stays the same).

Each filter is made of a few attributes, (of which two are required: the
`content` selector and the `next_chap` selector).

