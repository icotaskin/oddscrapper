import json
import requests
from bs4 import BeautifulSoup

pref = 'http://fb.oddsportal.com/feed/match/'
decoder = json.JSONDecoder(object_hook=None, parse_float=None, parse_int=None,
                           parse_constant=None, strict=True, object_pairs_hook=None)

def get_page(xeid, xhash, tipe):
    '''
    get html text from remote page
    1-3-UX19OwXR-5-1-yja8d.dat?_=1415473715925
    1-3-UX19OwXR-3-1-yja8d.dat?_=1415473649648
    1-3-UX19OwXR-2-1-yja8d.dat?_=1415473649648
    '''
    tipe_dict = {'line': '-3-1-', 'hcap': '-5-1-', 'total':'-2-1-'}
    link = pref + '1-3-' + xeid + tipe_dict[tipe] + xhash + '.dat'
    r = requests.get(link)
    #globals.jsonpCallback('/feed/match/1-3-UX19OwXR-3-1-yja8d.dat', ');'
    json_string = str(r.content)[63:-2]
    dic_obj = decoder.decode(json_string)
    return dic_obj['d']['oddsdata']['back'] 

def map_odds(odds_arry):
    arr_len = len(odds_arry)
    home, away = 0, 0
    if type(odds_arry[0]) is list:                
        home = sum([val[0] for val in odds_arry]) / arr_len
        away = sum([val[1] for val in odds_arry]) / arr_len
    else:
        home = sum([val['0'] for val in odds_arry]) / arr_len
        away = sum([val['1'] for val in odds_arry]) / arr_len
    return {
        'length': arr_len,
        'home': round(home, 2),
        'away': round(away, 2),
        'delta': round(abs(home - away), 2),
        }

def line(xeid, xhash):
    odds_dict = get_page(xeid, xhash, 'line')['E-3-1-0-0-0']['odds']
    odds_arry = [odds_dict[item] for item in odds_dict]
    data = map_odds(odds_arry)
    return [       
        data['home'],
        data['away'],
        type(odds_arry[0])
    ]

def hcap(xeid, xhash):
    arry = []
    odds_dict = get_page(xeid, xhash, 'hcap')
    for key, val in odds_dict.iteritems():
        hcap_value = float(val["handicapValue"])
        odds_dict = val['odds']
        odds_arry = [odds_dict[item] for item in odds_dict]
        if hcap_value % 1 != 0:
            data = map_odds(odds_arry)
            arry.append([
                data['length'],
                (float(hcap_value), -1 * float(hcap_value)),
                (data['home'], data['away']),
                data['delta'],
                type(odds_arry[0])
            ])
    sort_arry = sorted(arry, key=lambda k: k[3], reverse=False)
    return sort_arry[0] if sort_arry[0][0] > 10 else sort_arry[1]

def totl(xeid, xhash):
    arry = []
    odds_dict = get_page(xeid, xhash, 'total')
    for key, val in odds_dict.iteritems():
        hcap_value = float(val["handicapValue"])
        odds_dict = val['odds']
        odds_arry = [odds_dict[item] for item in odds_dict]
        if hcap_value % 1 != 0:
            data = map_odds(odds_arry)
            arry.append([
                data['length'],
                float(hcap_value),
                (data['home'], data['away']),
                data['delta'],
                type(odds_arry[0])
            ])
    sort_arry = sorted(arry, key=lambda k: k[3], reverse=False)
    return sort_arry[0] if sort_arry[0][0] > 10 else sort_arry[1]

def itot(handy, total):
    home, away = 0, 0
    hand = abs(handy[1][0])
    half = (total[1] - abs(handy[1][0])) / 2
    if half % 1 == 0:
        if handy[1][0] < 0:
            return [half + hand, half + 0.5]
        else:
            return [half + 0.5, half + hand]
    else:
        if handy[1][0] < 0:
            return [half + hand - 0.5, half]
        else:
            return [half, half + hand - 0.5]

if __name__ == '__main__':
    ''' scrap data from results table in browser console
        var elements = document.getElementsByClassName('deactivate');
        for (var i=0; i< elements.length; i += 1) {
            var res = elements[i].getElementsByTagName('a')[0].getAttribute('href');
            console.log(res.substring(20).trim());}
    '''
    url = [
        'golden-state-warriors-san-antonio-spurs-WbTfeRfO/',
        'portland-trail-blazers-charlotte-hornets-lzvjd7uI/',
        'dallas-mavericks-sacramento-kings-AquncmQB/',
        'memphis-grizzlies-los-angeles-lakers-OStva9ea/',
        'milwaukee-bucks-oklahoma-city-thunder-2JurbTA5/',
        'toronto-raptors-orlando-magic-E743z0hn/',
        'los-angeles-clippers-san-antonio-spurs-t4iZaktg/',
        'chicago-bulls-detroit-pistons-S0mV0VQn/',
        'new-york-knicks-atlanta-hawks-YwlR1BBt/',
        'cleveland-cavaliers-new-orleans-pelicans-KdsFff4D/',
        'indiana-pacers-utah-jazz-dEQcJwsE/',
        'los-angeles-lakers-charlotte-hornets-t6rBezk7/',
        'portland-trail-blazers-denver-nuggets-nqq7dGZ0/',
        'phoenix-suns-golden-state-warriors-z9u3cdKf/',
        'dallas-mavericks-miami-heat-hpjbbx5l/',
        'oklahoma-city-thunder-sacramento-kings-EgifaIkr/',
        'toronto-raptors-philadelphia-76ers-040aytwt/',
        'detroit-pistons-utah-jazz-M1aS3bsR/',
        'brooklyn-nets-orlando-magic-rB0O4vSK/',
        'milwaukee-bucks-memphis-grizzlies-nq7F60c8/',
        'san-antonio-spurs-new-orleans-pelicans-0nBJ5KCE/',
        'chicago-bulls-boston-celtics-fkKTrc51/',
        'houston-rockets-golden-state-warriors-YuJXsHK7/',
        'atlanta-hawks-new-york-knicks-lxkTpJzk/',
        'miami-heat-minnesota-timberwolves-SSmXqwje/',
        'indiana-pacers-washington-wizards-fFkPoaLr/',
        'los-angeles-clippers-portland-trail-blazers-IgbcjuDR/',
        'denver-nuggets-cleveland-cavaliers-zV8hiLcL/',
        'phoenix-suns-sacramento-kings-S45pgsT8/',
        'utah-jazz-dallas-mavericks-dvAlh1rF/',
        'oklahoma-city-thunder-memphis-grizzlies-lE6tfND2/',
        'boston-celtics-indiana-pacers-zZOgWJLe/',
        'brooklyn-nets-new-york-knicks-tCPkXa6k/',
        'detroit-pistons-milwaukee-bucks-n9ScVwy2/',
        'toronto-raptors-washington-wizards-zsZhGd7U/',
        'charlotte-hornets-atlanta-hawks-rypFw2TL/',
        'orlando-magic-minnesota-timberwolves-MRrJxMrS/',
        'philadelphia-76ers-chicago-bulls-2LQoYuiq/',
        'portland-trail-blazers-dallas-mavericks-lEpBvrEF/',
        'houston-rockets-san-antonio-spurs-zBt7uOb9/',
        'golden-state-warriors-los-angeles-clippers-hni2t4q3/',
        'sacramento-kings-denver-nuggets-EehbspUd/',
        'phoenix-suns-memphis-grizzlies-8b5CJtxj/',
        'utah-jazz-cleveland-cavaliers-nk4GI0id/',
        'san-antonio-spurs-atlanta-hawks-QZF7KMMq/',
        'milwaukee-bucks-chicago-bulls-fiPyQraM/',
        'washington-wizards-indiana-pacers-lEOuP2ES/',
        'boston-celtics-toronto-raptors-djzkHxhO/',
        'brooklyn-nets-minnesota-timberwolves-bPVSR4U9/',
        'detroit-pistons-new-york-knicks-G0QXQOqG/',
    ]
    full = 'http://www.oddsportal.com/basketball/usa/nba/'
    for i, u in enumerate(url):
        if i < 5:
            xeid = u[-9:][0:8] # get xeid from link
            #print full + u
            p = requests.get(full + u)
            poup = BeautifulSoup(p.content)
            text = str(poup)
            frst = text.find('xhash') + 8
            last = text.find('xhashf') - 3
            xhash = str(text[frst:last])
            # use threads!!!
            ln = line(xeid, xhash)
            hc = hcap(xeid, xhash)
            tl = totl(xeid, xhash)
            print ln, '\n', hc, '\n', tl, '\n', itot(hc, tl), '\n\n'
