iTunesMapper - Paul Mccombs
===========================

This project is not complete.

The goal is to import itunes XML file and google location data to produce a map of where you listened to what.

I'm using xml.etree.ElementTree to parse the iTunes XML file. I'm using json to parse the google location data.

Currently I have code to turn 'iTunes Music Library.xml' into a dictionary of Tracks and a dictionary of Play Lists. Currently all play Lists are parsed including Library which is not exposed in the iTunes user interface.

Currently I have code to extract the location data from google. The user will need to obtain the data from google themselves. I'm not likely to implement the screen scraping that seems to be neccesary to automate that.

I haven't found an obvous library for doing the spatial computations for interpolating position between time points. Found haversine implementations online to compute distance, but not to calculate bearing, and to locate a new point with bearing and distance.

I'm considering using ogr and fiona to export geoJSON output, but may just construct the files using basic string and file . 

I'm Planning to create a geoJSON file and use GitHub to display results. See: https://github.com/keum/data_display/blob/master/cso_test_file.geojson 

Historic notes:
---------------

I was planning to leverage liamks/pyitunes to get data from iTunes, but it doesn't seem to accomodate relating playlist tracks to the main track records.

License info:
-------------

Copyright (C) 2015  paul mccombs
contact at https://github.com/mccombsp-kingco/itunesmapper

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses/ .