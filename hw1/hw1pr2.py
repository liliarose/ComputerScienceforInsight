# starting examples for cs35, week2 "Web as Input"
import requests
import string
import json
import os
import webbrowser

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Problem 2 starter code
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# myFunctions: 
    # gets info for 2 artists & returns the id of the artist w/ more albums&singles 
    # prints the important info (see function)
    # creates a html/bootstrap page for the artists  
    # creates a site w/ all of the artist info together
    # website w/ multiple pages for all of the artists??? 
def getArtistData(slType, parameters):
    """
        gets the artist data as json, but doesn't store it 
    """
    search_url = "https://itunes.apple.com/"
    result = requests.get(search_url + slType, params=parameters)
    return result.json()

def saveFile(filename, content):
    """ 
        writes content into a file w/ filename
    """
    f = open(filename, "w" )     
    f.write(content)                        
    f.close()                                   

def apple_api(artist_name):
    """ 
        returns the id of the first artist that appears & saves the data into appledata.json
    """
    # uses the function to get artist info in json format
    parameters = {"term":artist_name,"entity":"musicArtist","media":"music","limit":200}
    data = getArtistData("search", parameters)
    # save to a local file so we can examine it
    filename_to_save = "appledata.json"
    string_data = json.dumps( data, indent=2 )  # this writes it to a string
    saveFile(filename_to_save, string_data)
    #print("\nfile", filename_to_save, "written.")
     #Here, you should return the artist id:
    return data["results"][0]["artistId"] 

def apple_api_lookup(artistId):
    """ 
    Takes an artistId and grabs a full set of that artist's albums.
    Then saves the results to the file "appledata_full.json"
    This function is complete, though you'll likely have to modify it
    to write more_productive( , ) ...
    """
    parameters = {"entity":"album","id":artistId}
    data = getArtistData("lookup", parameters)
    print("got data from web")
    # save to a file to examine it...
    filename_to_save="appledata_full.json"
    string_data = json.dumps( data, indent=2 )  # this writes it to a string
    saveFile(filename_to_save, string_data)
    #print("\nfile", filename_to_save, "written.")
    # we'll leave the processing to another function...
    return

def openfile(filename):
    """ 
        opens a file and returns its contents in json format
    """
    try:
        f = open(filename, "r", encoding="utf-8" )
        string_data = f.read()
        return json.loads(string_data)
    except FileNotFoundError:
        print("FileNotFoundError")

def apple_api_lookup_process():
    """ 
        example opening and accessing a large appledata_full.json file...
    """
    data = openfile("appledata_full.json")
    #try:
    try:
        pass
        #print("Unorganized data: ", data)
    except UnicodeEncodeError as err:
        print("If you're on Windows, then...", "\n  (1) Exit python", "\n  (2) Run chcp 65001 at the prompt", "\n  (3) Restart python and run... .")
    # for live investigation, here's the full data structure
    #print("finished apple_api_lookup")
    return data

def more_productive(artist1, artist2):
    """ 
        take the names, as strings, of two artists as input, converts those names to AppleIDs (notice that this requires an API call!) 
        and then makes another API call in order to gather all of the album/work information from iTunes 
        saves the info into a file w/ the name in the following format: artist + [artistID] + .json
        returns the 2 artist's id in a tuple
    """
    parameters1 = {"term":artist1,"entity":"musicArtist","media":"music","limit":200}
    artist1 = getArtistData("search", parameters1)
    artist1ID = str(artist1["results"][0]["artistId"])
    print("just got data(ID) for artist 1", artist1ID)
    # print(artist1)
    parameters2 = {"term":artist1,"entity":"musicArtist","media":"music","limit":200}
    artist2 = getArtistData("search", parameters2)
    artist2ID = str(artist2["results"][0]["artistId"])
    print("just got data(ID) for artist 2", artist2ID)
    # print(artist2)
    # save to a local file so we can examine it
    parameters1_1 = {"entity":"album","id":artist1ID}
    data1 = getArtistData("lookup", parameters1_1)
    parameters2_1 = {"entity":"album","id":artist2ID}
    data2 = getArtistData("lookup", parameters2_1)
    file1name = "artist"+artist1ID+".json"
    file2name = "artist"+artist2ID+".json"
    content1 = json.dumps(data1, indent=2)  # this writes it to a string
    #print(content1)
    content2 = json.dumps(data2, indent=2) 
    # print(content2)
    saveFile(file1name, content1)
    saveFile(file2name, content2)
    # Here, you should return the artist id:
    return (artist1ID, artist2ID)

def producesMore(artist1, artist2):
    """
        returns the artist that produces more albums & the #  
    """
    artistID = more_productive(artist1, artist2)
    file1name = "artist"+artistID[0]+".json"
    file2name = "artist"+artistID[1]+".json"
    content1 = openfile(file1name)
    content2 = openfile(file2name)
    albumNum1 = content1["resultCount"] - 1
    albumNum2 = content2["resultCount"] - 1
    if albumNum1 > albumNum2:
        return (artist1, artistID[0], albumNum1)
    elif albumNum1 < albumNum2:
        return (artist2, artistID[1], albumNum2)
    return [(artist1, artistID[0], albumNum1), (artist2, artistID[1], albumNum2)] 

def most_productive(listOfArtist):
    """ 
        gets a list of artists & then gets their ID & then saves their stuff into a file
        then returns a list of IDs 
    """
    artistsID = []
    for artist in listOfArtist: 
        param = {"term":artist,"entity":"musicArtist","media":"music","limit":200}
        sdata = getArtistData("search", param)
        artistID = str(sdata["results"][0]["artistId"])
        artistsID.append(artistID)
        print("just got data(ID) for", artist)
        
        param2 = {"entity":"album","id":artistID}
        ldata = getArtistData("lookup", param2)
        filename = "artist"+artistID+".json"
        content = json.dumps(ldata, indent=2)
        saveFile(filename, content)
        
        print("saved info for", artist, "at", filename)
    return artistsID

def printSdata(artistID):
    """
        gets a single artist's ID & prints the artist's name, his/her albums & # of songs & releaseDate & primaryGenreName & links to the iTunes page 
    returns a string w/ a neat format 
    """
    # get data 
    filename = "artist"+artistID+".json"
    data = openfile(filename)
    # artist's name & ID & link to iTunes page
    artistDataStr = data["results"][0]["artistName"] + " ("+str(data["results"][0]["artistId"])+")\n"
    artistDataStr += "link to iTunes: " + data["results"][0]["artistLinkUrl"] + "\n"
    artistDataStr += "primary genre: " + data["results"][0]["primaryGenreName"]  + "\n"
    artistDataStr += "total albums: " + str(data["resultCount"]-1)
    print(artistDataStr)
    
    # his/her albums & # of songs & releaseDate & primaryGenreName & links to the iTunes page 
    for i in range(1, len(data["results"])):
        print(data["results"][i]["collectionName"], "-", data["results"][i]["trackCount"], "songs")
        print("released @", data["results"][i]["releaseDate"])
        try:
            print("price:", data["results"][i]["collectionPrice"], data["results"][i]["currency"])
        except KeyError:
            pass
        print("iTunes link:", data["results"][i]["collectionViewUrl"])
        print()

def printData(listOfArtistID):
    """
        gets a list of artistID 
        prints the artist's name, his/her albums & # of songs & releaseDate & primaryGenreName & links to the iTunes page 
    """
    for artistID in listOfArtistID:
        printSdata(artistID)
    print("finished printing\n")

head = '<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css"><script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script><script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script></head><body><div class="container">'
end = '</div></body></html>'

def createPageContent(artistID):
    """
        input = artistID, the header part for the file & ending part for the file 
        creates content w/ collapses (w/ bootstrap) w/ the artist's name, his/her albums & # of songs & releaseDate & primaryGenreName & 
        links to the iTunes page, etc.  
        returns a string that can be made into an html file 
    """
    # get data
    filenameOpened = "artist"+artistID+".json"
    data = openfile(filenameOpened)
    # name
    content = "<h2>" + str(data["results"][0]["artistName"]) + "</h2>" # name #
    content+= "<p>(" +str(data["results"][0]["artistId"]) +")</p>" # ID #
    content+= '<p> <a target="_blank" href="'+data["results"][0]["artistLinkUrl"] +'"><strong>iTunes link</strong></a> | ' # itunes link #
    content+= data["results"][0]["primaryGenreName"] # genre #  
    content+= " | Albums & Singles: "+ str(data["resultCount"]-1) + "</p>" # album # 
    content+= '<div class="panel-group" id="accordion' + artistID + '">'
    for i in range(1, len(data["results"])):
        if i%2 == 1:
            content+= '<div class="row">'
        content+= '<div class="col-sm-6"><div class="panel panel-default panel-info"> <div class="panel-heading"> <h3 class="panel-title"> <a data-toggle="collapse" data-parent="#accordion' + artistID + '" href="#collapse' + artistID+ str(i)+'">'
        content+= str(data["results"][i]["collectionName"]) + '</a> </h3> </div>' # album title 
        content+= '<div id="collapse' + artistID + str(i)+'"class="panel-collapse collapse"> <div class="panel-body">'
        content+= '# of songs: ' + str(data["results"][i]["trackCount"])+ '<br>' # trackCount # 
        content+= 'release date: ' + data["results"][i]["releaseDate"][:10] + '<br>' # releaseDate #
        content+= 'genre: ' + data["results"][i]["primaryGenreName"]+ '<br>' # primaryGenreName # 
        content+= '<a target="_blank" href="'+data["results"][i]["collectionViewUrl"] + '">|iTunes Link|</a><br>' 
        try:
            content+= 'price: ' + str(data["results"][i]["collectionPrice"]) +' ' + data["results"][i]["currency"] + '<br>' # money #
        except KeyError:
            print(data["results"][i]["collectionName"], "doesn't have a price") 
        content+= 'copyright: ' + data["results"][i]["copyright"] + '<br>' # copyright # 
        content+= '</div></div></div></div>' # <div class="col-lg-1></div>'
        if i%2 == 0:
            content+= '</div>' 
        # print("finished adding album:", str(data["results"][i]["collectionName"]))  
    if len(data["results"])%2 == 0:
     content+= '</div>'
    content+="</div>" #</div>\n"
    return content 

def createPage(artistID, header=head, ending=end, path="."):
    """
        input = artistID, the header part for the file & ending part for the file 
        creates content w/ collapses (w/ bootstrap) w/ the artist's name, his/her albums & # of songs & releaseDate & primaryGenreName & 
        links to the iTunes page, etc.  
        returns the path of the file 
    """
    content = createPageContent(artistID) 
    filenameSaved = "artist"+artistID+".html"
    saveFile(path+"/"+filenameSaved, header+content+ending)
    print("create html file:", filenameSaved)
    return os.getcwd()+"/"+path+"/"+filenameSaved

def createAndOpenPages(listofID, filePrefix, created=False):
    """
        given a list of IDs, checks if they're created or not, if not, create them, if created, just open the pages 
        note: common errors --> not adding "file://" to the beginning & "/" to the end 
    """
    if not created:
        for ID in listofID:
            webbrowser.open("file://" + createPage(ID))
        return 
    for ID in listofID:
        filename = "artist"+ID+".html"
        try:
            webbrowser.open(filePrefix + filename)
        except FileNotFoundError:
            print("this file was not found:", filename)

def createOnePage(listofID, fileID="0", path="."):
   """
        creates one page for all artists instead of one page for each artists & then returns the address  
   """
   # nav bar / tabs
   content ='<h1> Artists </h1> <ul class="nav nav-tabs">'
   for i in listofID:
    filenameOpened = "artist"+i+".json"
    data = openfile(filenameOpened)
    content += ' <li><a data-toggle="tab" href="#artist' + i + '"><h4>'
    content += str(data["results"][0]["artistName"]) + '</h4></a></li>' 
   content += '</ul>'
   #tab panes
   content += '<div class="tab-content">' 
   for i in listofID:
    content += '<div id="artist' + i +'" class="tab-pane fade">'
    content += createPageContent(i)
    content += '</div>'
   content += '</div>'
   """
   """
   filenameSaved = "artists"+fileID+".html"
   saveFile(path+"/"+filenameSaved, head+content+end) # dependent on the global variables head & end
   print("create html file:", filenameSaved)
   return os.getcwd()+"/"+path+"/"+filenameSaved

def main():
    """ a top-level function for testing things... """
    # routine for getting the artistId
    if 1:
        artistId = apple_api("The Beatles") # should return 136975
        artistId = apple_api("Kendrick Lamar") # should return 368183298
        artistId = apple_api("Taylor Swift") # should return 159260351
        artistId = apple_api("Maroon 5") # should return 1798556
        print("artistId is", artistId)

    if 0:
        apple_api_lookup(159260351)
        data = apple_api_lookup_process()
        # return data

 # more_productive testing 
    if 0:
        print(more_productive("Katy Perry", "Steve Perry"))
        print("\n", more_productive("Jay Chou", "Jolin Tsai"))
    
    
    testingCompProduction = False # testing comparing album production # & the printing stuff out  
    if testingCompProduction:
        test = producesMore("Katy Perry", "Steve Perry")
        if len(test) == 3:
            printSdata(test[1])
        else:
            printData([test[0][1], test[1][1]])
    
    createdPages = False # SHOULD BE FALSE THE 1st TIME RUNNING THIS CODE ON YOUR COMPUTER & technically true after the 1st time 
    testing = True
    testingMultiWebPages = False 
    testingOnePageCreation = True 
    if testing:
        listofArtists = ["Katy Perry", "Steve Perry", "Jay Chou", "Jolin Tsai", "The Beatles", "Taylor Swift","Sam Smith","JJ Lin", "May Day"]
        listofArtistsID = most_productive(listofArtists)
        if testingMultiWebPages:
            createAndOpenPages(listofArtistsID, "file://"+os.getcwd()+"/", createdPages)
        if testingOnePageCreation:
            webbrowser.open("file://" + createOnePage(listofArtistsID))
        # remember to rm artist* to clear all the files made after testing stuff 
    """
    webbrowser.open("file://" + createPage("300117743")) # Jay Chou
    webbrowser.open("file://" + createPage("369211611"))  # May Day 
    webbrowser.open("file://" + createPage("136975")) # the Beatles
    webbrowser.open("file://" + createPage("159260351")) # Taylor Swift
    """ 
# passing the mic (of control) over to Python here...
#
if __name__ == "__main__":
    data = main()

