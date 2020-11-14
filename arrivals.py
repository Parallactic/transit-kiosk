#!/usr/bin/python

import cta
import metra
import uchicago

import json
import ConfigParser

config_file = r'config.cfg'

config = ConfigParser.ConfigParser()
config.read(config_file)

def main():
    cta_arrivals = cta.get_cta()
    #metra_arrivals = metra.get_metra()
    uchicago_arrivals = uchicago.get_uchicago()

    bus_arrivals = cta_arrivals + uchicago_arrivals

    #arrivals = bus_arrivals + metra_arrivals
    arrivals = bus_arrivals

    print("Content-Type: text/plain;charset=utf-8")
    print('')
    print json.dumps(arrivals)

if __name__ == "__main__":

    # calling main function
    main()
