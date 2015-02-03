iTunesMapper - Paul Mccombs
===========================

This project is not complete.

The goal is to import itunes XML file and google location data to produce a map of where you listened to what.

I'm using xml.etree.ElementTree to parse the iTunes XML file. I'm using json to parse the google location data.

Currently I have code to turn 'iTunes Music Library.xml' into a dictionary of Tracks and a dictionary of Play Lists. Currently all play Lists are parsed including Library which is not exposed in the iTunes user interface.

Currently I have code to extract the location data from google. The user will need to obtain the data from google themselves. I'm not likely to implement the screen scraping that seems to be neccesary to automate that.

I want to interpolate locations between two time points to map the time a song was played in iTunes. To accomplish this requires three tasks:

1. Given two latitude/longitude coordinate pairs; return a distance. I found this function in the geopy module: https://github.com/geopy/geopy , and in a gist: https://gist.github.com/jeromer/1883777

2. Given two latitude/longitude coordinate pairs; return a bearing. I found this function in a gist: https://gist.github.com/jeromer/2005586.

3. Given a latitude/longitude coordinate, a bearing, and a distance; return a latitude/longitude coordinate. I found this function in geopy. See example: http://stackoverflow.com/questions/7222382/get-lat-long-given-current-point-distance-and-bearing
_
    import geopy
    from geopy.distance import VincentyDistance
    
    # given: lat1, lon1, b = bearing in degrees, d = distance in kilometers
    
    origin = geopy.Point(lat1, lon1)
    destination = VincentyDistance(kilometers=d).destination(origin, b)
    
    lat2, lon2 = destination.latitude, destination.longitude

I'm considering using ogr and fiona to export geoJSON output, but may just construct the files using basic string and file.

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
