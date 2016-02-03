from urllib.request import FancyURLopener
from bs4 import BeautifulSoup
from random import choice
import csv
from time import sleep


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

    urls = list()
    url = "http://www.metacritic.com/browse/tv/score/metascore/year/all?sort=desc&year_selected=2015&page={}"
    for i in range(0,3):
        urls.append(url.format(i))
    return urls

def get_shows():

    with open('meta_critic.csv', 'w') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        writer.writerow(["rank", "score", "name", "user_score", "date"])

        for url in tv_urls():
            sleep(1)
            html =  myopener.open(url)
            html = html.read()
            bs_obj = BeautifulSoup(html, "html5lib")
            div = bs_obj.select("div.product_rows > div.product_row")
            for row in  div:
                rank  = row.select("div.row_num")[0].contents[0].strip().replace(".","")
                score = row.select("div.product_score > div.metascore_w")[0].contents[0].strip()
                name  = row.select("div.product_title > a")[0].get('href').split("/tv/")[-1].strip()
                user_score = row.select("span.textscore")[0].contents[0].strip()
                date = row.select("div.product_date")[0].contents[0].strip().replace(",", ";")
                fields = [rank, score, name, user_score, date]
                writer.writerows([fields])



get_shows()
