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

    #debug# for date in loc_tups:
    #debug#     print date[2]

    order_pos = bisect.bisect(loc_dates, time_point)
    before = loc_dates[order_pos -1]
    after = loc_dates[order_pos]
    locs_time_interval = after - before
    before_time_point_interval = time_point - before
    before_ratio = ((float(before_time_point_interval.days)*86400+
                          before_time_point_interval.seconds)/
                         (locs_time_interval.days*86400+locs_time_interval.seconds))
    lat_dist = (lats[order_pos]-lats[order_pos-1])
    lon_dist = (lons[order_pos]-lons[order_pos-1])
    interp_lat = lats[order_pos-1] + (lat_dist*before_ratio)
    interp_lon = lons[order_pos-1] + (lon_dist*before_ratio)
    interp_loc = (interp_lat,interp_lon)


    print locs[order_pos - 1], before
    print locs[order_pos], after
    #debug# print "Time between two locations:", locs_time_interval
    #debug# print "Time between before location and time point:", before_time_point_interval
    #debug# print "Ratio of before - time point to before - after:", before_ratio
    #debug# print "Latitude distance in 'degrees':", lat_dist
    #debug# print "Longitude distance in 'degrees':", lon_dist

    return interp_loc

if __name__ == '__main__':
    
    import library_parse_mod
    import glocations_parse_mod

    # Use library_parse_mod to bring in the users iTunes data.
    songs, plists = library_parse_mod.parse_XML()

    # Use glocations_parse_mod to bring in the Google Locations data.
    loc_tups = glocations_parse_mod.retreive_json_from_file()
    print len(loc_tups)
    print loc_tups[:2]

    for song in plists['Andre Bed Time']:
        play_date_UTC = songs[song]['Play Date UTC']
        interp_loc = cartesian_interpolation(play_date_UTC,loc_tups)

        print songs[song]['Name']," was last played at: ", interp_loc        


    #debug# print "time_point: " + str(time_point)

    # loc_tups = [(47.7644685, -122.3128514, datetime.datetime(2015, 1, 2, 20, 41, 15)),
    #             (47.7644339, -122.3128811, datetime.datetime(2015, 1, 14, 20, 36, 29)),
    #             (47.7644686, -122.3128513, datetime.datetime(2015, 1, 29, 20, 31, 33)),
    #             (47.7644697, -122.3128505, datetime.datetime(2015, 1, 29, 20, 45, 57)),
    #             (47.7644689, -122.3128500, datetime.datetime(2015, 1, 29, 20, 45, 42))]

