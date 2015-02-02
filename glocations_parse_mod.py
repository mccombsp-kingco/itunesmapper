# Portion of iTunesMapper. A project to parse the iTunes XML, import google
# location data, and create a map of where you listened to a subset of songs

# Copyright (C) 2015  paul mccombs
# contact at https://github.com/mccombsp-kingco/itunesmapper

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/ .

''' If you load this as a module call ????() with no arguments to get back a list of
    tupples representing timestamped locations that are retrieved from a Google
    Takeout LocationHistory.json file.
    
    Get your location data from google at https://www.google.com/settings/takeout
    Select your Location History with the json format option. Follow instructions
    and place the resulting file in the dirctory you run this file from.
'''

import datetime
import json

def retreive_json_from_file():
    ''' Call with no parameters. Returns a list of tupples in the form
        (lattitude, longitude, timestamp)
    '''
    with open ("LocationHistory.json") as handle:
        raw_json = json.load(handle)

    google_loc_list = []

    #debug# print len(raw_json['locations'])

    for google_loc in raw_json['locations']:
        out_tupple = (google_loc['latitudeE7']/10000000.0,
                      google_loc['longitudeE7']/10000000.0,
                      convert_date(google_loc['timestampMs']))
        google_loc_list.append(out_tupple)

    #debug# print len(google_loc_list)

    return google_loc_list

def convert_date(time_stamp):
    ''' call with one parameter a timestamp string from the google
        locations json file. returns a datetime.datetime object.
    '''
    return datetime.datetime.fromtimestamp(int(time_stamp) / 1000)

if __name__ == '__main__':
    print("Acquiring location data")

    google_loc_list = retreive_json_from_file()

    loc_length = len(google_loc_list)

    print str(loc_length)+" locations retrieved"

    print google_loc_list[0]
    print google_loc_list[loc_length-1]