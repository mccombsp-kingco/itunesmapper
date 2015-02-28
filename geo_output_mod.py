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

''' If you load this as a module call geojson(prop_list,data_list, file_name, 
    path_name) where prop_list
    is a list of strings representing the property names in the out put geojson
    file; data_list is a list of tupples containing a latitude coordinate, a
    longitude coordinate, and a value for each of the properties listed in 
    prop_list; file_name is a string containing the name of file to be created; and
    path_na e is a string with the path the file should be created in.
 
    It will attempt to create a file named file_name in path_name, and return a
    three element tupple with: a status integer (1 if successful and 0 if
    unsuccessful); a string containing the path and file name; a string containing
    any messages.
'''
def geojson(prop_list,data_list, file_name, path_name):
    #                 Example output
    # ================================================
    # {
    #   "type": "FeatureCollection",
    #   "features": [
    #     {
    #       "type": "Feature",
    #       "properties": {
    #         "marker-color": "#ff2f92",
    #         "marker-size": "medium",
    #         "marker-symbol": "",
    #         "name": "Little Bird, Little Bird"
    #       },
    #       "geometry": {
    #         "type": "Point",
    #         "coordinates": [
    #           -122.27971970295104,
    #           47.70029246496672
    #         ]
    #       }
    #     }
    #   ]
    # }
    return (0,None,"Not implemented")

if __name__ == '__main__':
    print "Does Nothing Yet!!"