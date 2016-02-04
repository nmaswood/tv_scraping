from urllib.request import FancyURLopener
from bs4 import BeautifulSoup
from random import choice
import csv
from time import sleep
from urllib.parse import quote
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

def tv_names():
    with open("meta_critic.csv", 'r') as infile:
        tv_reader = csv.reader(infile)
        next(tv_reader)
        shows = map(lambda x : '+'.join(x[2].split("-")), tv_reader)
        shows = map(lambda x : quote(x), shows)
        shows = map(lambda x : x.replace("%2B", "+"), shows)
        shows = list(shows)
    return shows

def fetch_api_data():

    show_data = list()


    for show_encoding in tv_names():
        url ='http://www.imdb.com/xml/find?json=1&mv=on&q={}'.format(show_encoding)
        try:
            html =  myopener.open(url)
            string_data = html.read().decode('utf-8')
            json_data = json.loads(string_data)
        except:
            print("fuck.{}".format(show_encoding))
            json_data = "ERROR"

        show_data.append({
            "show" : show_encoding,
            "data" : json_data
            })
        print (show_data)
        sleep(1)
        break

    with open("imdb_raw_data.json", "w") as outfile:
        json.dump(show_data, outfile)

fetch_api_data()
