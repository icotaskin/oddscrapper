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

import requests, time
from bs4 import BeautifulSoup
from docopt import docopt

args = docopt(__doc__, version='0.1.6')
link = ['http://www.oddsportal.com', '/basketball/usa/nba-', '/results/page/']
seas = {'14/15': '2014-2015', '13/14': '2013-2014', '12/13': '2012-2013',
        '11/12': '2011-2012', '10/11': '2010-2011', '09/10': '2009-2010',
        '08/09': '2008-2009', '07/08': '2007-2008', '06/07': '2006-2007'}

def seasoner(arg):
    if arg == ' - Play Offs': return 'play offs'
    elif arg == ' - Pre-season': return 'pre-season'
    else: return 'undefined'

if args['hist'] is True:
    
    frst_page = 1 if args['--first'] is None else int(args['--first'])
    last_page = 50 if args['--last'] is None else int(args['--last'])
    
    if last_page < frst_page:
        print 'First page is bigger than last!'
        raise TypeError
    for x in xrange(frst_page, last_page):
        url = link[0] + link [1] + seas[args['<season>']] + link[2] + str(x) + '/'
        r = requests.get(url)
        r.encoding = 'ISO-8859-1'
        soup = BeautifulSoup(r.content)
        yes = soup.find(id='tournamentTable').find(class_='cms')
        if yes:
            '''
            If unexisting last page with
            !No data available massage
            '''
            print x, r.status_code, yes.string
            break
        else:
            #print x, url, r.status_code, 'Some data'
            try:
                for tr in soup.find(id='tournamentTable').find('tbody').contents:
                    date, tipe, match = '', '', {}
                    clss = tr.get('class')      
                    if len(clss) == 2:
                        if clss[1] == 'nob-border':
                            tipe = tr.contents[0].text
                        elif clss[1] == 'deactivate':
                            t_data = tr.contents
                            #data['datetime'] = datetime.strptime(html_date, "%A, %d %b %Y, %H:%M")
                            try:
                                match['team'] = str(t_data[1].find('a').text).split(' - ')
                            except Exception, e:
                                print 'Teams error: \n', tr.prettify()
                                raise e
                            try:
                                match['xeid'] = str(tr.get('xeid'))
                            except Exception, e:
                                print 'xeid  error: \n', tr.prettify()
                                raise e
                            try:
                                match['tipe'] = 'Season' if len(tipe) == 0 else seasoner(tipe)
                            except Exception, e:
                                print 'Tipe error: \n', tr.prettify()
                                raise e
                            try:
                                match['link'] = str(t_data[1].find('a').get('href'))
                            except Exception, e:
                                print 'Link error: \n', tr.prettify()
                                raise e
                            try:
                                url2 = link[0] + match['link']
                                p = requests.get(url2)
                                p.encoding = 'ISO-8859-1'
                                poup = BeautifulSoup(p.content)
                                
                                try:
                                    '''
                                    getting 'xhash' obrezaja text
                                    '''
                                    text = str(poup)
                                    frst = text.find('xhash') + 8
                                    last = text.find('xhashf') - 3
                                    match['hash'] = text[frst:last]
                                except Exception, e:
                                    print 'xhash Error'
                                    raise e
                                try:
                                    '''
                                    <p class="result">
                                      [0] <span class="bold">Final result </span>
                                      [1] <strong>103:100&nbsp;OT&nbsp;(95:95)</strong>
                                      [2] (27:25, 17:25, 21:25, 30:20, 8:5)
                                    </p>
                                    'ascii' codec can't encode character u'\xa0' in position 7: ordinal not in range(128)
                                    '''
                                    status = poup.find(id='event-status')
                                    match['resalt'] = [int(x) for x in str(status.strong.text).split(':')]
                                    match['resbox'] = str(status.p.contents[2]).replace('(', '').replace(')', '')
                                    match['ot'] = False if len(match['resbox'].split(', ')) == 4 else True
                                except Exception, e:
                                    print 'Results Error'
                                    raise e
                            except Exception, e:
                                print 'On match error'
                                raise e
                            print match, '\n'
            except Exception, e:
                raise e
else:
    '''
    For Last console arguments
    '''
    pass

'''
for key, val in args.iteritems():
    print key, val
'''
