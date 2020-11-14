#!/usr/bin/python

import requests
import xml.etree.ElementTree as ET
import json
import re

def get_metra():

    pretty_stops = {'55TH-56TH-57TH': '55th-56th-57th St.',
                    'MCCORMICK': 'McCormick Place'}


    stops = ['55-56-57TH']
    local = ['MCCORMICK'] # <-- train stops here implies local, otherwise express
    routes = ['ME']

    metra_arrivals=[]

    url = 'https://gtfsapi.metrarail.com/gtfs/tripUpdates'
    resp = requests.get(url, auth=('f143591e1c46f0854acffc73cca2893a', '137b8cdc1a7d2abc8d0b07edbd7fb4a5'))

    trips = resp.json()

    for trip in trips:
        print trip['id']
        last_stop = '??'
        islocal = False
        if trip['trip_update']['trip']['route_id'] in routes:
            ar = {}
            #stu = "stop time update"
            for stu in trip['trip_update']['stop_time_update']:
              if stu['stop_id'] in stops:
                print stu['departure']['time']['low'], int(stu['departure']['delay'])/60
                #ar['departure'] = stu['departure']['low']
              if stu['stop_id'] in local:
                islocal = True
            if ar != {}:
              ar['dest'] = stu['stop_id']
            if ar != {}:
                print ar['departure']
                

    return metra_arrivals

def main():

    metra_arrivals = get_metra()

    arrivals = metra_arrivals

    print("Content-Type: text/plain;charset=utf-8")
    print('')
    print json.dumps(arrivals)

if __name__ == "__main__":

    # calling main function
    main()
