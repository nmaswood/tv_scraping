from urllib.request import urlopen
import json
from time import sleep


def tv_show_data():

    shows = list()

    with open ("tv_shows.txt", "r") as in_file:
        for line in in_file:
            shows.append(line)
    processed = map( lambda x :  x.split("/shows/")[-1], shows)
    processed = map(lambda x: x.strip("\n"), processed)
    processed = map(lambda x: x.strip(" "), processed)
    processed = map(lambda x: x.strip("\\"), processed)
    processed = map(lambda x: x.strip("/"), processed)
    processed = filter(lambda x: x != "", processed)
    processed = filter(lambda x: "sort" not in  x, processed)

    return list(processed)

def get_data_from_api():


    total_data = list()
    time_outs = list()

    shows = tv_show_data()
    shows = map(lambda x:  '+'.join(x.split("-")), shows)
    for i, show in enumerate(shows):
        print (i)
        try:
            request = urlopen('http://www.omdbapi.com/?t={}&y=&plot=short&r=json'.format(show))
            string_data = request.read().decode('utf-8')
            json_data = json.loads(string_data)
            total_data.append(
                    {
                        "show":  show,
                        "data" : json_data
                        })
        except:
            time_outs.append(show)

        sleep(1)

    with open('shows.json', 'w' ) as outfile:
        json.dump(total_data, outfile)
    with open('timeout.json', 'w') as outfile:
        json.dump(time_outs, outfile)


print  (len(tv_show_data()))

#get_data_from_api()
