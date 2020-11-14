#!/usr/bin/python

import requests
import re
import ConfigParser

config_file = r'config.cfg'

config = ConfigParser.ConfigParser()
config.read(config_file)

def get_uchicago():
    uchicago_arrivals = []

    stops = ['8062400', #55+LP wb
             '8062460', #57+SI metra2
             '8173082',#57+SI metra
             '8058068', #57+SI se corner
             '8062060',   #55+LP se corner
             '8204754', #55+HP sb
             '8062476', #harper court
             '8062516'] #55+LP eb

    for stop in stops:
        url = config.get('Transit', 'uchicago_bus_tracker_url') + stop
        resp = requests.get(url)

        #                <td class="wait_time time_1" width="110px"><a href="/t/routes/8002428" title="View all of 53rd Street Express">29 <abbr title="minutes">mins</abbr></a></td>

        matches = re.findall('<td class="wait_time.* width="110px"><a href="/t/routes/([0-9]*)" title="View all of (.*)"><?([0-9]*) &? ?([0-9]*) ?<abbr title="minutes">mins</abbr></a></td>', resp.text)

        for m in matches:
          try:
            ar = {}
            ar['dest'] = '??'
            ar['agency'] = 'uchicago'
            ar['stop'] = stop
            ar['route'] = m[1]
            if ar['route'] == '53rd Street Express':
              ar['route'] = '53rd'
            if ar['route'] == 'South Loop Shuttle':
              ar['route'] = 'Loop'
            if ar['route'] == 'Friend Center/Metra':
              ar['route'] = 'Friend'
            if ar['route'] == 'Midway Metra PM' or ar['route'] == 'Midway Metra AM':
              ar['route'] = 'Midway'
            if ar['stop'] == '8062400' and ar['route'] == 'East':
                ar['dest'] = '<span style="font-size: 110%;">Campus</span> <span style="font-size: 70%">via 55th/Woodlawn</span>'
            if ar['stop'] == '8204754' and ar['route'] == 'East':
                ar['dest'] = '<span style="font-size: 110%;">Campus</span> <span style="font-size: 70%">via 55th/Woodlawn</span>'
            if ar['stop'] == '8173082' and ar['route'] == 'Central':
                ar['dest'] = '<span style="font-size: 110%;">Campus</span> <span style="font-size: 80%">(via 60th/Ellis)</span>'
            if ar['stop'] == '8062460' and ar['route'] == 'Friend':
                ar['dest'] = 'Friend Center via Hospital'
                ar['dest'] = '<span style="font-size: 110%;">55th/Drexel</span> <span style="font-size: 80%">(via Hospital)</span>'
            if ar['stop'] == '8062516' and ar['route'] == 'Friend':
                ar['dest'] = 'Hospital via 59th'
            if ar['stop'] == '8062460' and ar['route'] == 'Metra':
                ar['dest'] = 'Hospital via 59th'
            if ar['stop'] == '8062460' and ar['route'] == 'Friend':
                ar['dest'] = 'Friend Center via Hospital'
                ar['dest'] = '<span style="font-size: 110%;">Friend Center</span> <span style="font-size: 80%">(via Hospital)</span>'
                ar['dest'] = '<span style="font-size: 110%;">55th/Drexel</span> <span style="font-size: 80%">(via Hospital)</span>'
            if ar['stop'] == '8058068' and ar['route'] == '53rd':
                ar['dest'] = 'Harper Court'
            if ar['stop'] == '8062060' and ar['route'] == '53rd':
                ar['dest'] = 'Harper Court'
            if ar['stop'] == '8062476' and ar['route'] == '53rd':
                ar['dest'] = '<span style="font-size: 110%;">Campus</span> <span style="font-size: 80%">(via 53rd/Ellis)</span>'
            if (ar['stop'] == '8062460' or ar['stop'] == '8173082') and ar['route'] == 'Midway':
                ar['dest'] = 'Campus'
            if ar['stop'] == '8173082' and ar['route'] == 'Loop':
                ar['dest'] = 'Roosevelt L'
            try:
                ar['mins'] = m[2]
            except:
                ar['mins'] = -1
            artwo = ar.copy()
            try:
                artwo['mins'] = m[3]
            except:
                ar['mins'] = -1

            uchicago_arrivals.append(ar)
            if artwo['mins'] != '':
              uchicago_arrivals.append(artwo)

            if ar['stop'] == '8173082' and ar['route'] == 'Central':
              arthree = ar.copy()
              arfour = artwo.copy()
              arthree['stop'] = '8062460a' #'8173082a'
              arfour['stop'] = '8062460a' #'8173082a'
              arthree['mins'] = int(ar['mins']) - 1
              arfour['mins'] = int(artwo['mins']) - 1
              uchicago_arrivals.append(arthree)
              uchicago_arrivals.append(arfour)

            if ar['stop'] == '8062400' and ar['route'] == 'East':
              arthree = ar.copy()
              arfour = artwo.copy()
              arthree['stop'] = '8062400a' #'8173082a'
              arfour['stop'] = '8062400a' #'8173082a'
              arthree['mins'] = int(ar['mins']) - 1
              arfour['mins'] = int(artwo['mins']) - 1
              uchicago_arrivals.append(arthree)
              uchicago_arrivals.append(arfour)

          except:
            next

    return sorted(uchicago_arrivals, key=lambda a: int(a['mins']))
