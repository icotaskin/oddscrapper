import requests, json
import numpy as np

pref = 'http://fb.oddsportal.com/feed/match/'
decoder = json.JSONDecoder(object_hook=None, parse_float=None,
    parse_int=None, parse_constant=None, strict=True, object_pairs_hook=None)

def line(xeid, xhash):
    #1-3-UX19OwXR-3-1-yja8d.dat?_=1415473649648
    link = pref + '1-3-' + xeid + '-3-1-' + xhash + '.dat'
    r = requests.get(link)
    # 63: globals.jsonpCallback('/feed/match/1-3-UX19OwXR-3-1-yja8d.dat', 
    # -2: );
    json_string = str(r.content)[63:-2]
    dic_obj = decoder.decode(json_string)
    if dic_obj['d']['E'] == "notAllowed":
        print 'Ecses not Allowed'
        raise TypeError
    arry = [val for key, val in dic_obj['d']['oddsdata']['back']['E-3-1-0-0-0']['odds'].iteritems()]
    mean = np.array(arry).mean(axis=0)
    print mean

def hcap(xeid, xhash):
	#1-3-UX19OwXR-5-1-yja8d.dat?_=1415473715925
    link = pref + '1-3-' + xeid + '-5-1-' + xhash + '.dat'
    r = requests.get(link)
    # 63: globals.jsonpCallback('/feed/match/1-3-UX19OwXR-3-1-yja8d.dat', 
    # -2: );
    json_string = str(r.content)[63:-2]
    dic_obj = decoder.decode(json_string)
    if dic_obj['d']['E'] == "notAllowed":
        print 'Ecses not Allowed'
        raise TypeError
    for key, val in dic_obj['d']['oddsdata']['back'].iteritems():
        print val['handicapValue'], '\n', val['odds'], '\n'

def totl(xeid, xhash):
	#1-3-UX19OwXR-2-1-yja8d.dat?_=1415473743131
	pass

if __name__ == '__main__':
    hcap('zV8hiLcL', 'yj333')
