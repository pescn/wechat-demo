# -*- coding: utf-8 -*-
import urllib2
import requests

def main(postid):
    r = urllib2.urlopen('http://www.kuaidi100.com/autonumber/autoComNum?text='+postid) 
    h = r.read()
    k = eval(h)
    kuaidicom = k["auto"][0]['comCode']
    
    setting = {'type': kuaidicom,'postid': postid}
    url = "http://m.kuaidi100.com/index_all.html?" + str(urllib.urlencode(setting))
    return url