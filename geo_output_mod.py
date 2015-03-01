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
    is a list of strings representing the property names in the output geojson
    file; data_list is a list of tupples containing a latitude coordinate, a
    longitude coordinate, and a value for each of the properties listed in 
    prop_list; file_name is a string containing the name of file to be created; and
    path_name is a string with the path the file should be created in.
 
    It will attempt to create a file named file_name in path_name, and return a
    three element tupple with: a status integer (1 if successful and 0 if
    unsuccessful); a string containing the path and file name; a string containing
    any messages.
'''
import os
import sys

def write_line(handle,string):
    handle.write(string+'\n')

def geojson(prop_list, data_list, file_name, path_name):
    ''' geojson(prop_list, data_list,file_name, path_name) outputs a geojson file given
        the inputs.
    '''
    # Start building components of the return object
    return_message = ''
    return_status = 0

    # create the full path and file name of the output file
    path_file = os.path.join(path_name, file_name)

    # list of lines that go at the begining of the geojson file
    start_list = ['{','  "type": "FeatureCollection",','  "features": [']

    # list of lines that go at the end of the geojson file
    end_list = ['  ]','}']

    # start writing a new file with the provided data. This will currently overwrite
    # an existing file with that name and location
    try:
        with open(path_file, 'w') as handle:
            for line in start_list:
                write_line(handle,line)

            first_record = True
            for record in data_list:
                # if this isn't the first record write out a comma to separate records
                if not first_record:
                    write_line(handle,',')

                first_record = False

                # write the prelinary bits of one Feature

                # write the properties from the records
                for record_prop in zip(prop_list,record[2:]):
                    write_line(handle,str(record_prop))

                # write the begining of the geometry portion of the feature

                # write the longitue then the latitude. NOT A TYPO

                #write the ending brackets for the feature

            for line in end_list:
                write_line(handle,line)

            # Set the return status to 1 indicating a successful file write.
            return_status = 1
    except:
        return_message = return_message+'Exception:\n'+str(sys.exc_info()[1])+'\n'
        #debug# raise
        

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

    if return_message == '':
        return_message = 'This string intentionaly left blank'
    return (return_status,path_file,return_message)

if __name__ == '__main__':
    print "Call this as a module."