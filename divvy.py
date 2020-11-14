#!/usr/bin/python
# coding=utf-8

import requests
#import xml.etree.ElementTree as ET
import json
import re
from math import radians, degrees, sin, cos, asin, acos, sqrt
from geopy.geocoders import GoogleV3
import cgi
import ConfigParser

config_file = r'config.cfg'

config = ConfigParser.ConfigParser()
config.read(config_file)

def dist_in_blocks(meters): #return distance in chicago city blocks, 200 meters = 1 block
  if meters <= 25: # 1/8 block or less
    return "0"
  if meters <= 75: # 1/8 - 3/8 blocks
    return "¼"
  if meters <= 125: # 3/8 - 5/8 blocks
    return "½"
  if meters <= 175: # 5/8 - 7/8 blocks
    return "¾"
  if meters <= 250: # 7/8 -1.25 blocks
    return "1"
  if meters <= 350: # 1.25 - 1.75 blocks
    return "1½"
  if meters <= 500: # 1.75 - 2.5 blocks
    return "2"
  if meters <= 700: # 2.5 - 3.5 blocks
    return "3"
  # 3.5+ blocks
  return "4+"

def google_minutes(lat1, lon1, lat2, lon2): # return walking distance in minutes and meters
  google_key = config.get('Google', 'google_maps_api_key')
  latlon1 = str(lat1) + "," + str(lon1)
  latlon2 = str(lat2) + "," + str(lon2)
  url = config.get('Google', 'google_maps_directions_url') + '?mode=walking&origin=' + latlon1 + '&destination=' + latlon2 + '&key=' + google_key
  resp = requests.get(url)
  minutes = json.loads(resp.content)['routes'][0]['legs'][0]['duration']['value'] / 60 # minutes
  meters = json.loads(resp.content)['routes'][0]['legs'][0]['distance']['value'] # always meters
  return minutes, meters

def google_address(lat, lon): # return a human readable address
  google_key = config.get('Google', 'google_maps_api_key')
  latlon = str(lat) + "," + str(lon)
  url = config.get('Google', 'google_maps_geocode_url') + '?latlng=' + latlon + '&result_type=street_address&key=' + google_key
  resp = requests.get(url)
  #print url
  results = json.loads(resp.content)['results'][0]['formatted_address']
  return results

def great_circle(lat1, lon1, lat2, lon2): # return great circle distance between two points
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    return 6371000 * ( acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2)) ) # spherical great circle distance in meters

def get_nearby_ebikes(lat, lon, num): #return the nearest [num] ebikes near lat, lon annotated distance and human readable addresses

    url = config.get('Bikeshare', 'divvy_undocked_bikes_url')
    resp = requests.get(url)
    bikes = json.loads(resp.content)['data']['bikes']

    for bike in bikes:
      #bike['distance'] = abs(bike['lat'] - lat) + abs(bike['lon'] - lon) # taxi cab metric approximates chicago's grid
      bike['distance'] = great_circle(lat, lon, bike['lat'], bike['lon'])

    bikes = [bike for bike in bikes if not (bike['is_reserved'] == 1 or bike['is_disabled'] == 1)]  #filter bikes that aren't available

    near_bikes = sorted(bikes, key=lambda x: x['distance']) # sort by distance

    near_bikes = near_bikes[:num] # return only the nearest [num] bikes

    for bike in near_bikes: # only hit geocode API for bikes that are reasonably close
      bike['address'] = google_address(bike['lat'], bike['lon']) # give it a human readable address
      bike['minutes'], bike['meters'] = google_minutes(lat, lon, bike['lat'], bike['lon']) # minutes walking
      bike['distance_blocks'] = dist_in_blocks(bike['meters'])

    near_bikes = sorted(near_bikes, key=lambda x: x['minutes']) # sort by walking time

    return near_bikes

def main():

    print("Content-Type: text/plain;charset=utf-8")
    print('')

    num = 5

    arguments = cgi.FieldStorage()

    try:
      address = arguments['address'].value
      google_key = config.get('Google', 'google_maps_api_key')
      url = config.get('Google', 'google_maps_geocode_url') + '?address=' + address  + '&key=' + google_key  + '&bounds=41.6405963,-87.8415993|42.0128091,-87.4981599' #only find stuff in Chicago area
      resp = requests.get(url)
      lat = json.loads(resp.content)['results'][0]['geometry']['location']['lat']
      lon = json.loads(resp.content)['results'][0]['geometry']['location']['lng']

    except:
      # no address
      lat = 41.7950533
      lon = -87.5851167
    
    near_bikes = get_nearby_ebikes(lat, lon, num)

    print json.dumps(near_bikes)

if __name__ == "__main__":

    # calling main function
    main()
