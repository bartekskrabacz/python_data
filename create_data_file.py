import json
import re
import urllib2
from math import *
import sys

#dane: moc, liczba czestotliwosci, macierz sasiedztwa

def main():
    data = import_date_from_btsearch((sys.argv[2], sys.argv[3]), (sys.argv[4], sys.argv[5]))
    #data = import_date_from_btsearch((50.039419, 21.382406), (50.063861, 21.400986))
    orig_stdout = sys.stdout
    f = open('data.data', "w")
    sys.stdout = f
    print "data;"
    print "param C_count := ", sys.argv[1], ";"
    print "param V_count := ", len(data["objects"]), ";"
    print "Param : A :="
    neighborhood_matrix(data, sys.argv[6])
    print ";"
    print "end;"
    sys.stdout = orig_stdout
    f.close()

def neighborhood_matrix(data, power):
    data=data["objects"]
    i = 0
    j = 0
    for station_one in data:
        length = len(data)
        i = data.index(station_one) + 1
        for station_two in data:
            id1 = station_one["id"]
            j=data.index(station_two) + 1
            id2 = station_two["id"]
            latitude_station_1 = station_one["latitude"]
            longitude_station_1 = station_one["longitude"]
            latitude_station_2 = station_two["latitude"]
            longitude_station_2 = station_two["longitude"]
            distance = greatCircleDistance((latitude_station_1, longitude_station_1), (latitude_station_2, longitude_station_2)) * 6371
            distance_factor = 0.33
            power = float(power)
            if distance < power*distance_factor:
                is_neighbour = 1
                print i, ",", j," ", is_neighbour
                #print id1, id2, i, j, distance, is_neighbour

def greatCircleDistance((lat1, lon1), (lat2, lon2)):
    lat1 = float(lat1)
    lat2 = float(lat2)
    lon1 = float(lon1)
    lon2 = float(lon2)
    def haversin(x):
      return sin(x/2)**2
    return 2 * asin(sqrt(
        haversin(lat2-lat1) +
        cos(lat1) * cos(lat2) * haversin(lon2-lon1)))

def import_date_from_btsearch((lat1, lon1), (lat2, lon2)):
    URL1 = 'http://beta.btsearch.pl/map/ukelocations/?bounds=%s,%s,%s,%s' % (lat1, lon1, lat2, lon2)
    print URL1
    url = urllib2.urlopen(URL1)
    data = json.load(url)
    return data


# This is called first
if __name__ == '__main__':
    main()
