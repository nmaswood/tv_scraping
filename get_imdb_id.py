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

    for index,show_encoding in enumerate(tv_names()):
        print (index)
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
        sleep(1)

    with open("imdb_raw_data.json", "w") as outfile:
        json.dump(show_data, outfile)

#http://www.imdb.com/title/tt5045592/fullcredits?ref_=tt_ql_1

def get_id(i_json):

    popular = i_json.get("title_popular")
    exact = i_json.get("title_exact")
    substring = i_json.get("title_substring")

    if popular:

        for i_pop in popular:

            desc = i_pop.get("description")
            if desc:
                desc = desc.lower()
                if "tv" in desc:
                    return i_pop.get("id")

            title_desc = i_pop.get("title_description")
            if title_desc:
                title_desc = title_desc.lower()
                if "tv" in title_desc:
                    return i_pop.get("id")

    if exact:

        for i_exact in exact:

            desc = i_exact.get("description")
            if desc:
                desc = desc.lower()
                if "tv" in desc:
                    return i_exact.get("id")

            title_desc = i_exact.get("title_description")
            if title_desc:
                title_desc = title_desc.lower()
                if "tv" in title_desc:
                    return i_exact.get("id")

    if substring:

        for i_sub in substring:
            desc = i_sub.get("description")
            if desc:
                desc = desc.lower()
                if "tv" in desc:
                    return i_sub.get("id")
            title_desc = i_sub.get("title_description")
            if title_desc:
                title_desc = title_desc.lower()
                if "tv" in title_desc:
                    return i_exact.get("id")
    return "NO_ID"


def filter_original_data():

    valid = []
    invalid = []

    with open("imdb_raw_data.json", 'r') as infile:
        seen_data = json.load(infile)

    filter_data = filter(lambda x: x['data'] != "ERROR", seen_data)
    filter_data = list(filter_data)

    for json_unit in filter_data:
        show = json_unit['show']
        show_id = get_id(json_unit['data'])
        if show_id != "NO_ID":
            valid.append({
                "show": show,
                "show_id": show_id
                })
        else:
            invalid.append(show)

    with open("valid_show_id.json", 'w') as outfile:
        json.dump(valid, outfile)
    with open("invalid.json", 'w') as outfile:
        json.dump(invalid, outfile)

def redirects():

    redirects = []

    with open("imdb_raw_data.json", "r") as infile:
        seen_data = json.load(infile)

    filter_data = filter(lambda x: x["data"] == "ERROR", seen_data)

    urls = map(lambda x: x['show'], filter_data)
    urls = map(lambda x: 'http://www.imdb.com/xml/find?json=1&mv=on&q={}'.format(x), urls)
    urls = list(urls)

    print ("redirects")
    for index,show_encoding in enumerate(urls):
        print (index)

        html =  myopener.open(show_encoding)
        redirect = html.geturl() 
        show_name = show_encoding.split("&q=")[-1]

        redirects.append({
            "show" : show_name,
            "id" : redirect 
            })
        sleep(1)

    with open("redirects.json", 'w') as outfile:
        json.dump(redirects, outfile)

def consolidate():

    total = []

    manual_resolve =[

    {"show": "getting+on+2013","id": "tt2342652"},
    {"show": "marvels+jessica+jones","id": "tt2357547"},
    {"show": "the+flash+2014","id": "tt3107288"},
    {"show": "empire+2015","id": "tt3228904"},
    {"show": "house+of+cards+2013","id": "tt1856010"},
    {"show": "supergirl+2015","id": "tt4016454"},
    {"show": "episodes+us","id": "tt1582350"},
    {"show": "the+returned+2015","id": "tt3230780"},
    {"show": "ballers+2015","id": "tt2891574"},
    {"show": "the+spymasters+++cia+in+the+crosshairs","id": "tt4965308"},
    {"show": "funny+or+die+presents+americas+next+weatherman","id": "tt4965308"},
    {"show": "the+slap+2015","id": "tt3476576"},



    {"show": "sexdrugsrockroll","id": "tt3594982"},
    {"show": "scream+queens+2015","id": "tt4145384"},
    {"show": "limitless+2015","id": "tt4422836"},
    {"show": "allegiance+2015","id": "tt3581654"},
    {"show": "scream+2015","id": "tt3921180"},
    {"show": "12+monkeys+2015","id": "tt3148266"},
    {"show": "the+messengers+2015","id": "tt3513704"},
    {"show": "whitney+2015","id": "tt3750942"},
    {"show": "code+black+2015","id": "tt4452630"},
    {"show": "minority+report+2015","id": "tt4450826"},
    {"show": "the+odd+couple+2015","id": "tt3595776"},
    {"show": "truth+be+told+2015","id": "tt4481248"},
    {"show": "the-muppets-2015","id": "tt4651824"}
    ]

    with open("valid_show_id.json", 'r') as infile:
        valid_json = json.load(infile)
    with open("redirects.json", 'r') as infile:
        valid_json_2 = json.load(infile)

    new_list = []
    for item in valid_json_2:
        show = item['show']
        _id = item['id']
        _id = _id.split("/title/")[-1].strip("/")
        new_list.append({
            "show" : show,
            "show_id" : _id
            })


    total = valid_json + new_list + manual_resolve


    with open("final_id.json",'w') as outfile:
        json.dump(total,outfile)

def create_id_dict():

    show_to_id_dict = {} 
    with open("final_id.json", 'r') as infile:
        data = json.load(infile)

    for item in data:
        _id = item.get("id")
        if not _id:
            _id = item.get("show_id")
        show = '-'.join(item.get('show').split("+"))
        show = unquote(show)
        show_to_id_dict[show] = _id

    return show_to_id_dict

print (create_id_dict())

def id_to_meta():

    with open("meta_final.csv",'w') as outfile:
        csvwriter = csv.writer(outfile)
        csvwriter.writerow(['rank', 'score', 'name', 'season', 'user_score', 'date','imdb_id'])
        id_dict = create_id_dict()
        with open("meta_critic.csv") as csv_out:
            data = csv.reader(csv_out)
            next(data)
            for row in data:
                new_list = list()
                show = row[2]
                _id= id_dict.get(show)
                row.append(_id)
                if _id:
                    csvwriter.writerow(row)
                    #consolidate()
id_to_meta()