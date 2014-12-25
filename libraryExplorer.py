import xml.etree.ElementTree as et

# initialize and load the iTunes data from the XML file.
# using a copy of the file placed in my development directory for safe keeping.
lib = et.parse('iTunes Music Library.xml').getroot()

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
        return false
    elif tag_txt == 'true':
        return true
    elif tag_txt == 'string':
        return text_txt
    elif tag_txt == 'integer':
        return int(text_txt)
    elif tag_txt == 'date':
        return int(text_txt)
    else:
        return "Didn't expect a '%s' with value: %s" % (tag_txt, text_txt) 

def convert_song_el(song_el):
        '''Consumes a <dict> tag from source XML and returns a 2 element tuple. The 1st
           element is an integer containing the Track ID. The 2nd element is key & value pair
           to be added '''
        # This needs to be implemented obviously will not work yet.
        
        song_dict = {}
        alternator = 0 #This variable will alternate between 0 which indicates a key tag
        #               and 1 which indicates a value tag
        TrackID_flag = False #This variable will be set to true when the Track ID integer is 
        #                     expected.

        for attribute_el in song_element:
            if attribute_el.text == "TrackID":
                TrackID_flag = True
            <key>Track ID</key><integer>3536</integer>
            <key>Name</key><string>KEXP Live Performance Podcast: The Gossip</string>
            <key>Artist</key><string>The Gossip</string>
            <key>Album</key><string>KEXP Live Performances Podcast</string>
            <key>Genre</key><string>Podcast</string>
            <key>Kind</key><string>MPEG audio file</string>
            <key>Size</key><integer>27832978</integer>
            <key>Total Time</key><integer>1391544</integer>
            <key>Year</key><integer>2006</integer>
            <key>Date Modified</key><date>2006-03-05T20:01:25Z</date>
            <key>Date Added</key><date>2010-05-25T05:44:08Z</date>
            <key>Bit Rate</key><integer>160</integer>
            <key>Sample Rate</key><integer>48000</integer>
            <key>Play Date</key><integer>3224514089</integer>
            <key>Play Date UTC</key><date>2006-03-07T01:21:29Z</date>
            <key>Release Date</key><date>2006-02-24T21:34:00Z</date>
            <key>Sort Artist</key><string>Gossip</string>
            <key>Persistent ID</key><string>1B1440663BFF32B0</string>
            <key>Track Type</key><string>File</string>
            <key>Podcast</key><true/>
            <key>Unplayed</key><true/>
            <key>Location</key><string>file://localhost/Users/paulmccombs/Music/iTunes/iTunes%20Music/Podcasts/KEXP%20Live%20Performances%20Podcast/KEXP%20Live%20Performance%20Podcast_%20The%20Gossip.mp3</string>
            <key>File Folder Count</key><integer>4</integer>
            <key>Library Folder Count</key><integer>1</integer>


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
    #childprint(child)
    if prev_text == "Tracks" and child.tag == "dict":
        super_print("Found it!")
        songs = child
        break
    else:
        prev_text = child.text

# create a generator from the songs element
songs_gen = songs.iter()

#Convert the Tracklist <dict> element (songs variable) into a python structure.
#Every other child of songs is a <dict> element representing a track
#This block is untested.
songs_dict = {}
songs_gen.next() # this throws away the <key> tag
song_element = songs_gen.next() # this is the <dict> with the good stuff for one song.
(song_key, song_dict) = convert_song_el(song_element)
songs_dict[song_key] = song_dict
print songs_dict



#next steps:
#    That is the list of all tracks in the database,
#    convert it into a real dictionary with "Track ID"
#    as the key, and all the attributes as a tupple.







### disregard everything below for now
'''
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
#print "Play Lists: " + str(playlists)

# for song in lib.getPlaylist(playlists[12]).tracks:
#     print "[%d] %s - %s" % (song.number, song.artist, song.name)

songs_list = [(song.lastplayed, song.artist, song.name) for song in lib.getPlaylist(playlists[12]).tracks]
songs_header =["Date","Artist","Name"]

print "Least Recently Played Songs:"
for song1 in songs_list:
    print song1

print __table_choice__(songs_header,songs_list)
'''
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
