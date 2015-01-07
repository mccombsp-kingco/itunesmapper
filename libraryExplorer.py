import xml.etree.ElementTree as et
import datetime

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


def parse_XML():
    ''' parse_XML() takes no arguments. It currently loads a hard coded iTunes XML file.
        Checks its version. Uses ElementTree to parse the tree and create a root. Finds
        the Tracks <dict> tag that contains all the song data elements. Creates a iterator.
        Loops through the Tracks <dict> passing the iterator to song_value_dict which
        returns a 3 element tuple. The song_key (int), song_value_dict (dict of attribute
        elements for that song), and a boolean flag that indicates the end of the Tracks
        <dict> and breaks the loop. Finally returns a dictionary with each song_key and
        song_value_dict in it.
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
            break
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

    #This only goes through the first song. Needs to go into a loop and loop until
    # the end of the Tracks <dict>. Use while True: and break out when end is 
    # detected.
    while True:
        (song_key, song_dict, the_end) = convert_song_el(songs_gen)
        if the_end: # this indicates end of all song dicts
            break
        songs_dict[song_key] = song_dict
        #debug# print str(len(songs_dict))+" songs in the songs_dict: 2"
        #debug# print songs_dict
        #debug# print len(songs_dict[song_key])
        #debug# print songs_dict[song_key].keys()

    super_print(str(len(songs_dict))+" songs in the songs_dict.")

    return songs_dict

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


if __name__ == '__main__':
    super_print("Welcome to the Library Explorer!")
    parse_XML()
    
    #### implement the library Explorer functionality. May want to fix and use
    #### __table_choice__()

    ####  handle track lists next