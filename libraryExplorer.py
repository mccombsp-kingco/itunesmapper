# pyItunes is downloaded and placed somewhere that it is visible to your python
# install. I have added my git repository to my $PYTHONPATH variable.
# download from: https://github.com/liamks/pyitunes
from pyItunes import *

# initialize and load the iTunes data from the XML file.
# using a copy of the file placed in my development directory for safe keeping.
lib = Library("iTunes Music Library.xml")

# Sample code provided with pyItunes
# for id, song in lib.songs.items():
#     print song.name


def __table_choice__(header, body):

    """ input header (a list of strings) and body (a list of tuples) length of
    header should match length of all tuples."""

    length_list = []
    for head in header:
        length_list.append(len(head))

    for row in body:
        for idx, item in enumerate(row):
            length_list[idx] = max(length_list[idx],len(unicode(item)))

    return_string = str(length_list)

    for head in zip(header,length_list):
        print head[0].ljust(head[1], " "),
    print "".ljust(sum(length_list), "=")
    # print "Choice  ",
    # print "Date".ljust(12, " "),
    # print "Volunteer".ljust(21, " "),
    # print "Last Contacted".ljust(16, " "),
    # print "Notes"
    # for el in range(1,len(date_list)+1):
    #     choice_text = "  (%s)" % el
    #     print choice_text.ljust(8," "),
    #     print date_list[el-1][0].ljust(12," "),
    #     print date_list[el-1][1].ljust(21," "),
    #     print date_list[el-1][2].ljust(16," "),
    #     print date_list[el-1][3]

    # chooser = -1
    # start = 1
    # stop = len(date_list)
    # while chooser > stop or chooser < start:
    #     chooser = __get_choice__(start, stop)

    # print chooser

    # chooser_raw = raw_input("select a choice above (%s to %s) or Q to quit: " % (start, stop))
    # try:
    #     chooser = int(chooser_raw)
    # except:
    #     if chooser_raw.upper() == 'Q':
    #         raise KeyboardInterrupt
    #    print "Must choose a number."
    #     return -1

    # if chooser < start or chooser > stop:
    #      print "Number is out of range."
    #     return -1
    # else:
    #     return chooser
    return return_string



# Have user select play list to explore
playlists=lib.getPlaylistNames()

# for song in lib.getPlaylist(playlists[12]).tracks:
#     print "[%d] %s - %s" % (song.number, song.artist, song.name)

songs_list = [(song.number, song.artist, song.name) for song in lib.getPlaylist(playlists[12]).tracks]
songs_header =["Number","Artist","Name"]

print "songs_list"+str(type(songs_list))

print __table_choice__(songs_header,songs_list)

'''
Attributes of the Song class:

name (String)
artist (String)
album_artist (String)
composer = None (String)
album = None (String)
genre = None (String)
kind = None (String)
size = None (Integer)
total_time = None (Integer)
track_number = None (Integer)
track_count = None (Integer)
disc_number = None (Integer)
disc_count = None (Integer)
year = None (Integer)
date_modified = None (Time)
date_added = None (Time)
bit_rate = None (Integer)
sample_rate = None (Integer)
comments = None (String)
rating = None (Integer)
album_rating = None (Integer)
play_count = None (Integer)
location = None (String)
compilation = None (Boolean)
grouping = None (String)
lastplayed = None (Time)
length = None (Integer)
'''
