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

import datetime, bisect, math

''' If you load this as a module call cartesian_interpolation().
    cartesian_interpolation() takes a point in time and a list of tupples
    representing 
    timestamped locations. Each tupple contains a decimal degree latitude
    coordinate (float), a longitude coordinate (float), and datetime object.
    cartesian_interpolation() returns a latitude, longitude coordinate (tupple of
    floats).
    
    To do list:
    1. create an option for using spherical coordinate geometry to determine the
       interpolated location.
'''

def cartesian_interpolation(time_point, loc_tups):

    loc_tups = sorted(loc_tups, key=lambda loc: loc[2])

    lats, lons, loc_dates = zip(*loc_tups)

    locs = zip(lats, lons)

    after_pos = bisect.bisect(loc_dates, time_point)
    #debug# print "After Position", after_pos
    #debug# print "Length of Locs list", len(loc_dates)

    before_pos = after_pos-1

    # Check for dates that are before the location dates.
    if after_pos == 0:
        print "No data before"
        #debug# print locs[after_pos], loc_dates[after_pos]
        return locs[after_pos]

    # Check for dates that are after the location dates.
    if after_pos == len(loc_dates):
        #debug# print locs[before_pos], loc_dates[before_pos]
        print "No data after"
        return locs[before_pos]

    #debug# print locs[before_pos], loc_dates[before_pos]
    #debug# print locs[after_pos], loc_dates[after_pos]

    locs_time_interval = loc_dates[after_pos] - loc_dates[before_pos]
    before_time_point_interval = time_point - loc_dates[before_pos]
    before_ratio = ((float(before_time_point_interval.days)*86400+
                          before_time_point_interval.seconds)/
                         (locs_time_interval.days*86400+locs_time_interval.seconds))
    lat_dist = (lats[after_pos]-lats[before_pos])
    lon_dist = (lons[after_pos]-lons[before_pos])
    interp_lat = lats[before_pos] + (lat_dist*before_ratio)
    interp_lon = lons[before_pos] + (lon_dist*before_ratio)
    interp_loc = (interp_lat,interp_lon)

    return interp_loc

if __name__ == '__main__':
    
    import library_parse_mod
    import glocations_parse_mod
    import geo_output_mod

    # Use library_parse_mod to bring in the users iTunes data.
    songs, plists = library_parse_mod.parse_XML()

    # some sample data
    # gloc_tups = [(47.7644685, -122.3128514, datetime.datetime(2014, 11, 30, 20, 41, 15)),
    #             (47.7644339, -122.3128811, datetime.datetime(2014, 12, 14, 20, 36, 29)),
    #             (47.7644686, -122.3128513, datetime.datetime(2014, 10, 9, 20, 31, 33)),
    #             (47.7644697, -122.3128505, datetime.datetime(2014, 9, 2, 11, 45, 57)),
    #             (47.7644689, -122.3128500, datetime.datetime(2014, 6, 29, 20, 45, 42))]


    # Use glocations_parse_mod to bring in the Google Locations data.
    gloc_tups = glocations_parse_mod.retreive_json_from_file()

    output_properties = ["Name","Artist","Play Date","Album"]
    output_filename = "AndreBedTime.geojson"
    output_path = "."
    output_data = []

    for song in plists['Andre Bed Time']:
        play_date_UTC = songs[song]['Play Date UTC']
        interp_loc = cartesian_interpolation(play_date_UTC,gloc_tups)

        output_data.append((interp_loc[0],interp_loc[1],songs[song]['Name'],
                            songs[song]['Artist'],songs[song]['Play Date UTC'],
                            songs[song]['Album']))

    #debug# print output_data 
    return_obj = geo_output_mod.geojson(output_properties, output_data,
                                        output_filename, output_path)

    if return_obj[0] == 0:
        print return_obj[2]    
