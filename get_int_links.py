from urllib.request import FancyURLopener
from bs4 import BeautifulSoup
from random import choice
import csv

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

def tv_urls():

    url = "http://www.tv.com/shows/sort/a_z/category/game-show/decade/2010s/"
    urls = [url]
    for i in range(2,8):
        urls.append(url + "page{}/".format(i))
    return urls


def get_shows():




    for url in tv_urls():
        html =  myopener.open(url)
        html = html.read()
        bs_obj = BeautifulSoup(html, "html5")
        div = bs_obj.select("div._clearfix > ul > li > a")
        show_urls = map (lambda x: x.get('href'), div)
        print (list(a))

        break

get_shows()
