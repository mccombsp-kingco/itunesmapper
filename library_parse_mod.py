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

import xml.etree.ElementTree as et
import datetime

''' If you load this as a module call parse_XML() with no arguments to get back a two
    element tupple. First a songs dictionary and second a play list dictionary.
    
    To do list:
    1. Something things:
    for song in tester.values():
        if song.has_key('Artist') and song['Artist'] == 'Sufjan Stevens':
            print song['Album'], song['Name']
    for song in pl_dict["Andre Bed Time"]:
        print songs_dict[song]['Name']
        print songs_dict[song]['Play Date UTC']
            
    2. Implement the library Explorer functionality

    3. Make __table_choice__() work

    4. handle play lists            
'''

def childprint(child_el):
    '''Takes any ElementTree element object and prints out the tag, attrib and text'''
    print ''.ljust(50,'-')
    print child_el.tag
    print child_el.attrib
    print child_el.text
    print ''.ljust(50,'-')

def super_print(txt_input):
    print "".ljust(50, '#')
    print txt_input
    print "".ljust(50, '#')

def convert_text_to_data(tag_txt, text_txt):
    '''
    Take in the tag and text attributes of an element and convert the text
    to the data type indicated in the tag, as neccesary.
    Return the converted data.
    Check for following tag values:
        'false', 'string', 'dict', 'key', 'date', 'integer', 'true'   
    '''
    if tag_txt == 'false':
        return False
    elif tag_txt == 'true':
        return True
    elif tag_txt == 'string':
        return text_txt
    elif tag_txt == 'integer':
        return int(text_txt)
    elif tag_txt == 'date':
        return datetime.datetime.strptime(text_txt, '%Y-%m-%dT%H:%M:%SZ')
    else:
        return "Didn't expect a '%s' with value: %s" % (tag_txt, text_txt) 

def convert_song_el(songs_gen):
    '''uses elements from songs_gen established in main body logic and returns a 
       2 element tuple. The 1st
       element is an integer containing the Track ID. The 2nd element is a dict with key &
       value pairs derived from the children tags of the <dict> tag passed in. '''
    #### need to check if this will be <dict> on the 1st song or Track ID on the 2nd +
    #### need to predict and only run this line the first time.
    
    song_value_dict = {}
    alternator = 0 #This variable will alternate between 0 which indicates a key tag
    #               and 1 which indicates a value tag
    TrackID_flag = False #This variable will be set to true when the Track ID integer is 
    #                     expected.
    try:
        while True:
            attribute_el = songs_gen.next()
            #debug# print attribute_el.tag, attribute_el.text
            if attribute_el.tag == "dict": # this detects the start of the next song.
                break
            if attribute_el.text == "Track ID":
                TrackID_flag = True
                alternator = 1
            elif TrackID_flag == True:
                song_key = int(attribute_el.text)
                TrackID_flag = False
                alternator = 0
            elif alternator == 0:
                song_value_dict_key = attribute_el.text
                alternator = 1
            elif alternator == 1:
                song_value_dict_value = convert_text_to_data(attribute_el.tag, attribute_el.text)
                alternator = 0
                song_value_dict[song_value_dict_key] = song_value_dict_value
    except StopIteration: #This catches the end of the TrackList element
        #debug# print song_key
        return (song_key, song_value_dict, True)
        
    #debug# print song_key
    return (song_key, song_value_dict, False)

def convert_list_el(lists_gen):
    ''' Uses lists_gen.next() to step through the XML, find each play list,
        create a string of the name and a set of the Track ID integers then
        return them. Values of None will be
        returned to indicate the end of the play lists is reached.
    '''
    prev_el = lists_gen.next()
    #debug# childprint(prev_el)
    current_el = lists_gen.next()
    #debug# childprint(current_el)

    try:
        while True: # loop looking for Name element of play list, and the array
                    # tag that hold all the track ids
            if prev_el.tag == 'dict' and current_el.text == 'Name':
                #debug# super_print("test is true")
                current_el = lists_gen.next()
                #debug# childprint(current_el)
                plist_name = current_el.text
            if prev_el.text == 'Playlist Items' and current_el.tag == 'array':
                #debug# childprint(current_el)
                plist_gen = current_el.iter()
                break

            prev_el = current_el
            current_el = lists_gen.next()

        #create the set of Track IDs for playlist
        track_ids = set()
        plist_prev_el = plist_gen.next()
        #debug# print "plist_prev_el"
        #debug# childprint(plist_prev_el)

        for plist_current_el in plist_gen:
            #debug# childprint(plist_current_el)
            #debug# xxx = raw_input("wait")
            if plist_prev_el.text == 'Track ID' and plist_current_el.tag == 'integer':
                #debug# super_print("test is true")
                track_ids.add(int(plist_current_el.text))
                #debug# childprint(plist_current_el)

            plist_prev_el = plist_current_el        

    except StopIteration: #This catches the end of the Play List elements
        #debug# print "StopIteration caught"
        return (None,None)
        
    return (plist_name, track_ids)

def parse_XML():
    ''' parse_XML() takes no arguments. It currently loads a hard coded iTunes XML file.
        Checks its version. Uses ElementTree to parse the tree and create a root. Finds
        the Tracks <dict> tag that contains all the song data elements. Creates a iterator.
        Loops through the Tracks <dict> passing the iterator to song_value_dict which
        returns a 3 element tuple. The song_key (int), song_value_dict (dict of attribute
        elements for that song), and a boolean flag that indicates the end of the Tracks
        <dict> and breaks the loop. Finally returns a two object tupple. First a songs
        dictionary with SongID intergers for keys and song attribute dictionaries for
        values. Second a Play List Dictionary with string Names for keys, and set of
        SongIDs for values.
    '''

    # initialize and load the iTunes data from the XML file.
    # using a copy of the file placed in my development directory for safe keeping.
    lib = et.parse('iTunes Music Library.xml').getroot()

    # test that the XML version number is the one we know how to deal with.    
    version_num = lib.attrib["version"]
    if version_num == '1.0':
        super_print("Parsing iTunes XML version %s" % version_num)
    else:
        super_print("iTunes XML versioin %S, is not supported." % version_num)

    #lib[0] is the <dict> tag just under the lib <plist> tag set as the lib root
    #Looking for the <dict> tag that is preceded by the <key> tag with a text of
    #"Tracks" 
    prev_text = None
    for child in lib[0]:
        #debug# childprint(child)
        if prev_text == "Tracks" and child.tag == "dict":
            #debug# super_print("Found the 'Tracks' <dict> tag!")
            songs = child
        elif prev_text == "Playlists" and child.tag == "array":
            lists = child
            #debug# super_print("Found the 'Playlists' <array> tag!")
        else:
            prev_text = child.text

    # create a generator from the songs element
    songs_gen = songs.iter()
    #debug# super_print("songs_gen type:"+str(type(songs_gen)))

    #Convert the Tracklist <dict> element (songs variable) into a python structure.
    #Every other child of songs is a <dict> element representing a track
    songs_dict = {}
    songs_gen.next() # this throws away the root <dict> tag
    songs_gen.next() # this throws away the <key> tag
    songs_gen.next() # this brings us to the 1st of the single song <dict> tags

    # This loops until the end of the Tracks <dict> and passes each song element
    # to convert_song_el
    while True:
        (song_key, song_dict, the_end) = convert_song_el(songs_gen)
        songs_dict[song_key] = song_dict
        if the_end: # this indicates end of all song dicts
            break

    #debug# super_print(str(len(songs_dict))+" songs in the songs_dict.")

    # Get ready to parse the Play Lists
    play_list_dict = dict()
    #debug# super_print("pld1 "+str(play_list_dict))
    
    # create a generator from the playlist element
    lists_gen = lists.iter()

    # This loops until the end of the Playlists <array> and creates play_list_dict, a 
    # dictionary with a key/value pair for each playlist. The key is a string containing
    # the play list name. The value is a set of Track IDs.
    while True:
        (list_key, list_set) = convert_list_el(lists_gen)
        if not list_key: # this indicates end of all play list arrays
            break
        play_list_dict[list_key] = list_set
        #debug# super_print("pld2 "+str(play_list_dict))
        #debug# print "Play List: "+list_key+" - Length: "+str(len(list_set))


    return (songs_dict, play_list_dict)

def __table_choice__(header, body):

    """ NOT FUNCTIONAL Code: Input header (a list of strings) and body (a list of tuples) length of
    header should match length of all tuples."""

#     length_list = []
#     for head in header:
#         length_list.append(len(head))
# 
#     for row in body:
#         for idx, item in enumerate(row):
#             length_list[idx] = max(length_list[idx],len(unicode(item)))
# 
#     return_string = str(length_list)
# 
#     for head in zip(header,length_list):
#         print head[0].ljust(head[1], " "),
#     print "".ljust(sum(length_list), "=")
#     print "Choice  ",
#     print "Date".ljust(12, " "),
#     print "Volunteer".ljust(21, " "),
#     print "Last Contacted".ljust(16, " "),
#     print "Notes"
#     for el in range(1,len(date_list)+1):
#         choice_text = "  (%s)" % el
#         print choice_text.ljust(8," "),
#         print date_list[el-1][0].ljust(12," "),
#         print date_list[el-1][1].ljust(21," "),
#         print date_list[el-1][2].ljust(16," "),
#         print date_list[el-1][3]
# 
#     chooser = -1
#     start = 1
#     stop = len(date_list)
#     while chooser > stop or chooser < start:
#         chooser = __get_choice__(start, stop)
# 
#     print chooser
# 
#     chooser_raw = raw_input("select a choice above (%s to %s) or Q to quit: " % (start, stop))
#     try:
#         chooser = int(chooser_raw)
#     except:
#         if chooser_raw.upper() == 'Q':
#             raise KeyboardInterrupt
#        print "Must choose a number."
#         return -1
# 
#     if chooser < start or chooser > stop:
#          print "Number is out of range."
#         return -1
#     else:
#     
#     return return_string

def collect_keys(songs_dict):
    ''' Takes the dictionary of songs output by parse_XML, scans through all songs and
        makes a set including all of the possible attribute keys.
    '''
    song_keys = set()
    for song in songs_dict.values():
        for k in song.keys():
            song_keys.add(k)

    return song_keys

if __name__ == '__main__':
    super_print("Acquiring iTunes data")
    (all_songs, all_lists) = parse_XML()
    all_keys = collect_keys(all_songs)

    super_print(str(all_keys))
    #debug# super_print(str(all_lists))
    #debug# super_print(str(all_songs[169498]))
    for pl_name in all_lists.keys():
        print "Play List: "+pl_name+" - Length: "+str(len(all_lists[pl_name]))