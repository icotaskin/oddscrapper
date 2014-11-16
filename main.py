#!/usr/bin/env python
"""
Odds portal NBA scrapper

Usage:
    scrap.py hist -s <season> [-f <first>] [-l <last>]
    scrap.py last [-l <last>]
    scrap.py -d | --debug
    scrap.py -v | --version
    scrap.py -h | --help

Options:
    -s --season         Season.
    -f --first <first>  First page to scrap.
    -l --last <last>    Last page to scrap.
    -d --debug          Show debug messages.
    -h --help           Show this screen.
    -v --version        Show version.
"""

from docopt import docopt
from tablerows import table, rows
from odds import line, hcap, totl 




args = docopt(__doc__, version='0.1.7')
season = args['<season>']

if args['hist'] is True:

    frst_page = 1 if args['--first'] is None else int(args['--first'])
    last_page = 50 if args['--last'] is None else int(args['--last'])

    if last_page < frst_page:
        print 'First page is bigger than last!'
        raise TypeError
    
    for x in xrange(frst_page, last_page):
        
        # get html from remote page
        html_data = table(season, x)

        # iterate per match
        for row in rows(html_data):
            m = Match(row)
            # save m
