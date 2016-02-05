from urllib.request import FancyURLopener
from bs4 import BeautifulSoup
from random import choice
import csv
from time import sleep
from urllib.parse import quote,unquote
import json


user_agents = [
'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
'Opera/9.25 (Windows NT 5.1; U; en)',
'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
]

class MyOpener(FancyURLopener, object):
        version = choice(user_agents)

myopener = MyOpener()

def _ids():
    with open("meta_final.csv", 'r') as infile:
        tv_reader = csv.reader(infile)
        next(tv_reader)
        return list(map(lambda x : x[-1], tv_reader))

def fetch_cast_data():

    for index, _id in enumerate(_ids()):
        print (index)
        url ='http://www.imdb.com/title/{}/fullcredits?ref_=tt_ql_1'.format(_id)
        try:
            html =  myopener.open(url).read()
        except:
            html = "error"

        with open('data/' + _id + '.html', 'wb') as outfile:
            outfile.write(html)
        sleep(.5)

fetch_cast_data()