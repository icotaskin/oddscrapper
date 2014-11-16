import requests
from bs4 import BeautifulSoup
import datetime

link = ['http://www.oddsportal.com', '/basketball/usa/nba-', '/results/page/']
seas = {'14/15': '2014-2015', '13/14': '2013-2014', '12/13': '2012-2013',
        '11/12': '2011-2012', '10/11': '2010-2011', '09/10': '2009-2010',
        '08/09': '2008-2009', '07/08': '2007-2008', '06/07': '2006-2007'}

def tables(seas_arg, iks):
    """
    Scrap all data from resalts table
    """
    try:
        url = link[0] + link[1] + seas[seas_arg] + link[2] + str(iks) + '/'
        r = requests.get(url)
        if r.status_code != 200:
            print url
            print 'Error: status code is ', r.status_code
            table(seas_arg, iks)
        r.encoding = 'ISO-8859-1'
        soup = BeautifulSoup(r.content)
        if soup.find(id='tournamentTable').find(class_='cms'):
            print url,
            print 'Page haven\'t resalts table'
            tables(seas_arg, iks)
        return soup
    
    except Exception:
        print url
        print 'Something wrong in table function'
        table(seas_arg, iks)

def rows(soup):
    """
    Get data from table rows
    """
    try:
        seas_type = ''
        table_data = []
        for tr in soup.find(id='tournamentTable').find('tbody').contents:
            match = {}
            row_class = tr.get('class')      
            # [0] ['', 'deactivate']
            # [1] ['center', 'nob-border']
            # [3] ['table-dummyrow']
            # [4] [] --- ??? 
            # [5] ['dark', 'center']
            if len(row_class) == 2:
                if row_class[0] == 'center':
                    seas_type = str(tr.contents[0].text)
                    tipe = tr.contents[0].text
                elif row_class[1] == 'deactivate':
                    t_data = tr.contents

                    """   date & time   """
                    try:
                        #table-time datet t1397689200-1-1-0-0 
                        data = int(t_data[0].get('class')[2].split('-')[0][1:])
                        #2014-06-16 03:00:00
                        temp = datetime.datetime.fromtimestamp(data)
                        vremja = {
                            'timestamp': data,
                            'datetime': temp.strftime("%d %b %Y %H:%M"),
                            'date': temp.strftime("%d-%m-%y"), 
                            'time': temp.strftime("%H:%M"),
                        }
                        match['datetime'] = vremja
                        print temp.strftime("%Z  %z")
                    except Exception, e:
                        raise e

                    """ teams """
                    try:
                        teams = str(t_data[1].find('a').text).split(' - ')
                        if len(teams) == 2 and type(teams) == list \
                        and len(teams[0]) > 4 and len(teams[0]) > 4:
                            match['team'] = teams
                        else:
                            print 'Teams error'
                    except Exception, e:
                        print 'Teams error: \n', tr.prettify()
                        raise e
                    
                    """ xeid  """
                    try:
                        xeid = str(tr.get('xeid'))
                        if len(xeid) == 8:
                            match['xeid'] = xeid
                        else:
                            print 'Xeid error'
                    except Exception, e:
                        print 'xeid  error: \n', tr.prettify()
                        raise e
                    
                    """ game type """
                    try:
                        if seas_type == '':
                            match['tipe'] = 'season'
                        elif seas_type == ' - Play Offs':
                            match['tipe'] = 'play-offs'
                        elif seas_type == ' - Pre-season':
                            match['tipe'] = 'pre-season'
                        else:
                            print 'Can not get match type'
                    except Exception, e:
                        print 'Tipe error: \n', tr.prettify()
                        raise e
                    
                    """ link """
                    try:
                        match['link'] = str(t_data[1].find('a').get('href'))
                    except Exception, e:
                        print 'Link error: \n', tr.prettify()
                        raise e

                    """
                    get data from sigle match page
                    """
                    url2 = link[0] + match['link']
                    p = requests.get(url2)
                    p.encoding = 'ISO-8859-1'
                    # second 'soup' is 'borshch'
                    borshch = BeautifulSoup(p.content.replace('&nbsp', ' '))
                    
                    """   xhash   """
                    try:
                        text = str(borshch)
                        frst = text.find('xhash') + 8
                        last = text.find('xhashf') - 3
                        match['hash'] = text[frst:last]
                    except Exception, e:
                        print 'xhash Error'
                        raise e
                    '''
                    <p class="result">
                        [0] <span class="bold">Final result </span>
                        [1] <strong>109:108&nbsp;OT&nbsp;(99:99)</strong>
                        [2] (27:25, 17:25, 21:25, 30:20, 8:5)
                    </p>
                    '''
                    status = borshch.find(id='event-status')
                    
                    """ score """
                    try:
                        match['score'] = [int(x) for x in str(status.strong.text).split(' ')[0].split(':')]
                        match['res_box'] = str(status.p.contents[2]).replace('(', '').replace(')', '')
                        match['ot'] = False if len(match['res_box'].split(', ')) == 4 else True
                    except Exception, e:
                        print 'OT Error \n'
                        raise e
                        print match, '\n'

                    #print match
                    table_data.append(match)
        ''' {
            'ot': False,
            'hash': 'yj1b4',
            'xeid': '67Upolsm',
            'tipe': 'play-offs',
            'score': [104, 87],
            'link': '/basketball/usa/nba-2013-2014/san-antonio-spurs-miami-heat-67Upolsm/',
            'team': ['San Antonio Spurs', 'Miami Heat'],
            'res_box': ' 22:29, 25:11, 30:18, 27:29',
            'datetime': {
                'date': '11-06-14',
                'timestamp': 1402448400,
                'time': '04:00',
                'datetime': '11 Jun 2014 04:00'
            }
        }'''

        return table_data             
    except Exception, e:
        print 'rows() error'
        print e
        #rows(soup)

if __name__ == '__main__':
    rows(tables('13/14', 1))
