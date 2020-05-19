import json

import requests
from COVID19Py import COVID19
import itertools


def request(url, endpoint, params=None):
    if params is None:
        params = {}
    response = requests.get(url + endpoint, {**params})
    response.raise_for_status()
    return response.json()


def UpdateData():
    try:
        covid19 = COVID19()
        locations = covid19.getLocations(timelines=True)
        recovered = request("https://covid19api.herokuapp.com/", "recovered")
        for country in recovered['locations']:
            if country['province'] == 'nan':
                country['province'] = ''
            for location in locations:
                if country['country'] == location['country'] and country['province'] == location['province']:
                    location['latest']['recovered'] = country["latest"]
                    location['timelines']['recovered']["latest"] = country["latest"]
                    location['timelines']['recovered']["timeline"] = country["history"]
                    # for fromr, tor in zip(country["history"].items(),
                    #                       location['timelines']['recovered']["timeline"].items()):
                    #     location['timelines']['recovered']["timeline"][tor[0]] = country["history"][fromr[0]]
                    break

        with open('data.json', 'w') as outfile:
            json.dump(locations, outfile)
        outfile.close()
        return True
    except:
        print("Didn't Update")
        return False


def GetData():
    with open('data.json') as f:
        locations = json.load(f)
    f.close()
    return locations


def GetLatest():
    try:
        latest = request("https://covid19api.herokuapp.com/", "latest")
        with open('Latest.json', 'w') as outfile:
            json.dump(latest, outfile)
        outfile.close()
    except:
        with open('Latest.json') as f:
            latest = json.load(f)
        f.close()
    return latest


def GetSummary():
    try:
        Summary = request("https://api.covid19api.com/", "summary")
        with open('Summary.json', 'w') as outfile:
            json.dump(Summary, outfile)
        outfile.close()
    except:
        with open('Summary.json') as f:
            Summary = json.load(f)
        f.close()
    return Summary


def GenerateDailyData():
    with open('data.json') as f:
        data = json.load(f)
    f.close()
    for i in range(len(data)):
        previous = 0
        for j in data[i]['timelines']['confirmed']['timeline']:
            temp = previous
            previous = data[i]['timelines']['confirmed']['timeline'][j]
            data[i]['timelines']['confirmed']['timeline'][j] -= temp
            if data[i]['timelines']['confirmed']['timeline'][j] < 0:
                data[i]['timelines']['confirmed']['timeline'][j] = 0
        previous = 0
        for j in data[i]['timelines']['deaths']['timeline']:
            temp = previous
            previous = data[i]['timelines']['deaths']['timeline'][j]
            data[i]['timelines']['deaths']['timeline'][j] -= temp
            if data[i]['timelines']['deaths']['timeline'][j] < 0:
                data[i]['timelines']['deaths']['timeline'][j] = 0
        previous = 0
        for j in data[i]['timelines']['recovered']['timeline']:
            temp = previous
            previous = data[i]['timelines']['recovered']['timeline'][j]
            data[i]['timelines']['recovered']['timeline'][j] -= temp
            if data[i]['timelines']['recovered']['timeline'][j] < 0:
                data[i]['timelines']['recovered']['timeline'][j] = 0
    with open('daily.json', 'w') as outfile:
        json.dump(data, outfile)
    outfile.close()


def GetDailyData():
    with open('daily.json') as f:
        daily = json.load(f)
    f.close()
    return daily
