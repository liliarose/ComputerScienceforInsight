#
# starting examples for cs35, week2 "Web as Input"
#

import requests
import string
import json


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# Problem 2 starter code
#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#
#
#

def apple_api(artist_name):
    """ 
    """
    ### Use the search url to get an artist's itunes ID
    search_url = "https://itunes.apple.com/search"
    parameters = {"term":artist_name,"entity":"musicArtist","media":"music","limit":200}
    result = requests.get(search_url, params=parameters)
    data = result.json()

    # save to a local file so we can examine it
    filename_to_save = "appledata.json"
    f = open( filename_to_save, "w" )     # opens the file for writing
    string_data = json.dumps( data, indent=2 )  # this writes it to a string
    f.write(string_data)                        # then, writes that string to a file...
    f.close()                                   # and closes the file
    print("\nfile", filename_to_save, "written.")

    # Here, you should return the artist id:
    #
    # Note: it's helpful to find the iTunes artistId and return it here
    # (this hasn't been done yet... try it!) 

    return 42   # This is probably _not_ the correct answer...


#
# 
#
def apple_api_lookup(artistId):
    """ 
    Takes an artistId and grabs a full set of that artist's albums.
    "The Beatles"  has an id of 136975
    "Kendrick Lamar"  has an id of 368183298
    "Taylor Swift"  has an id of 159260351

    Then saves the results to the file "appledata_full.json"

    This function is complete, though you'll likely have to modify it
    to write more_productive( , ) ...
    """
    lookup_url = "https://itunes.apple.com/lookup"    
    parameters = {"entity":"album","id":artistId}    
    result = requests.get(lookup_url, params=parameters)
    data = result.json()

    # save to a file to examine it...
    filename_to_save="appledata_full.json"
    f = open( filename_to_save, "w" )     # opens the file for writing
    string_data = json.dumps( data, indent=2 )  # this writes it to a string
    f.write(string_data)                        # then, writes that string to a file...
    f.close()                                   # and closes the file
    print("\nfile", filename_to_save, "written.")

    # we'll leave the processing to another function...
    return



#
#
#
def apple_api_lookup_process():
    """ example opening and accessing a large appledata_full.json file...
        You'll likely want to do more!
    """
    filename_to_read="appledata_full.json"
    f = open( filename_to_read, "r", encoding="utf-8" )
    string_data = f.read()
    data = json.loads( string_data )
    #try:
    try:
        print("the raw json data is\n\n", data, "\n")
    except UnicodeEncodeError as err:
        print("If you're on Windows, then...")
        print("  (1) Exit python")
        print("  (2) Run    chcp 65001    at the prompt")
        print("  (3) Restart python and run... .")

    # for live investigation, here's the full data structure
    return data



#
# main()  for testing problem 2's functions...
#
def main():
    """ a top-level function for testing things... """
    # routine for getting the artistId
    if 0:
        #artistId = apple_api("The Beatles") # should return 136975
        #artistId = apple_api("Kendrick Lamar") # should return 368183298
        #artistId = apple_api("Taylor Swift") # should return 159260351
        artistId = apple_api("Maroon 5") # should return 1798556
        print("artistId is", artistId)

    if 1:
        #apple_api_lookup(1798556)
        data = apple_api_lookup_process()
        return data

    # more_productive( "Katy Perry", "Steve Perry" )
    # get each one's id
    # get each one's file
    # compare number of albums! Done!
    # then ask two of your own questions


#
# passing the mic (of control) over to Python here...
#
if __name__ == "__main__":
    data = main()


