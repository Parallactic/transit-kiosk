#!/usr/bin/python

import requests
import xml.etree.ElementTree as ET
import json
import re

import ConfigParser

config_file = r'config.cfg'

config = ConfigParser.ConfigParser()
config.read(config_file)

def loadRSS(url):

    resp = requests.get(url)

    return resp.content

def parse_cta_xml(xml): 
  
    # create element tree object 
    root = ET.fromstring(xml) 
    
    # create empty list for news items 
    arrivals = [] 
  
    # iterate news items 
    for item in root:
        if item.tag == "noPredictionMessage":
          continue
  
        # empty arrivals dictionary 
        arrival = {} 
  
        # iterate child elements of item 
        for child in item: 
            arrival[child.tag] = child.text
  
        # append arrivals dictionary to arrivals items list 
        arrivals.append(arrival) 
      
    # return news items list 
    return arrivals
  
def get_cta():

    stops = ['1654', #55+HP sb
            '1518', #55+HP nb
            '10566', #55+HP wb
            '10567', #55+LP wb
            '10563', #55+LP eb
            '7132', #55+LP nb
            '7059', #78 sb
            '1656', #57+LP sb
            '1515', #57+LP nb
            '7179', #55+LP sb
            '15919'] #shoreland

    cta_arrivals=[]

    for stop in stops:
        url =  config.get('Transit', 'cta_bus_tracker_url') + '?route=all&stop=' + stop
        content = loadRSS(url)

        # parse xml file
        stop_arrivals = parse_cta_xml(content)

        for ar in stop_arrivals:
            if 'noPredictionMessage' in ar.keys():
              continue
            try:
                ar['mins'] = int(ar['pt'])
            except:
                ar['mins'] = 0
            if ar['mins'] < 1:
                ar['mins'] = 0
            if ar['pu'] == 'DELAYED':
                ar['mins'] = -1
            ar['dest'] = ar['fd']
            ar['route'] = ar['rn']
            ar['stop'] = stop
            ar['agency'] = 'cta'
            if(ar['stop'] == '10566' and ar['route'] == '171'):
              artwo = {}
              artwo['stop'] = '10566a'
              artwo['dest'] = ar['dest']
              artwo['route'] = ar['route']
              artwo['mins'] = ar['mins']
              artwo['agency'] = ar['agency']
              cta_arrivals.append(artwo)
        cta_arrivals += stop_arrivals
    return cta_arrivals

def get_metra():
    metra_arrivals = []

    return metra_arrivals

