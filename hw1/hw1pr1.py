#
# starting examples for cs35, week1 "Web as Input"
import requests
import string
import json
import webbrowser
import os
"""
Examples to run for problem 1:
Web scraping, the basic command (Thanks, Prof. Medero!)
# basic use of requests:
url = "https://www.cs.hmc.edu/~dodds/demo.html"  # try it + source
result = requests.get(url)
text = result.text   # provides the source as a large string...
# try it for another site...
# let's try the Open Google Maps API -- also provides JSON-formatted data
#   See the webpage for the details and allowable use
# Try this one by hand - what are its parts?
# http://maps.googleapis.com/maps/api/distancematrix/json?origins=%22Claremont,%20CA%22&destinations=%22Seattle,%20WA%22&mode=%22walking%22
# Take a look at the result -- perhaps using this nice site for editing + display:
# A nice site for json display and editing:  https://jsoneditoronline.org/
"""
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Problem 1
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# example of calling the google distance API

def google_api(Sources, Dests, my_mode="driving"):
    """ Inputs: Sources is a list of starting places
                Dests is a list of ending places
        This function uses Google's distances API to find the distances
             from all Sources to all Dests. 
        It saves the result to distances.json
        Problem: right now it only works with the FIRST of each list!
    """
    print("Start of google_api")
    # https://maps.googleapis.com/maps/api/distancematrix/json?origins=Seattle&destinations=San+Francisco&key=AIzaSyAWit2nM8azitSxupwaV24DfGjCO1cKhfE
    if len(Sources) < 1 or len(Dests) < 1:
        print("Sources and Dests need to be lists of >= 1 city each!")
        return

    # API key - provided in class
    APIkey = "AIzaSyDfCduGlyctaJTIXbvMspmzteitocza4Tk"
    url ="https://maps.googleapis.com/maps/api/distancematrix/json"
    start = "|".join(Sources)
    end = "|".join(Dests)
    
    inputs={"origins":start,"destinations":end,"mode":my_mode,"key":APIkey}

    result = requests.get(url,params=inputs)
    data = result.json()
    print("data is", data)
    filename_to_save = "distances.json"
    f = open( filename_to_save, "w" )     # opens the file for writing
    string_data = json.dumps( data, indent=2 )  # this writes it to a string
    f.write(string_data)                        # then, writes that string to a file
    f.close()                                   # and closes the file
    print("\nFile", filename_to_save, "written.")
    # no need to return anything, since we're better off reading it from file later...
    return
# example of handling json data via Python's json dictionary

def printInfo(JD, infoType):
    # simplifies the json_process to get the info for distance & duration --> depends on the infoType
    dst = JD["destination_addresses"]
    src = JD["origin_addresses"]
    sCt = 0 # I hate python w/o nice for loops x(
    dCt = 0
    errorMessage = "PATH DOES NOT EXIST"
    while sCt < len(src):
        info = JD["rows"][0]["elements"]
        # assumes that for origin addresses, there exists no repetition
        dCt = 0
        print("From", src[sCt])
        while dCt < len(dst):
            if info[dCt]["status"] == "OK":
                print(" ... to", dst[dCt], "==", info[dCt][infoType]["text"])
            else:
                print(" ... to", dst[dCt], "==", errorMessage)
            dCt += 1
        print()
        sCt += 1

def json_process():
    """ This function reads the json data from "distances.json"
        It should build a formatted table of all pairwise distances.
        _You_ decide how to format that table (better than JSON!)
    """
    filename_to_read = "distances.json"
    f = open( filename_to_read, "r" )
    string_data = f.read()
    JD = json.loads( string_data )  # JD == "json dictionary"
    print("Distance Info:")
    printInfo(JD, "distance")
    print("Duration Info:")
    printInfo(JD, "duration")

def createPage():
    """ creates a new html page & creates a table """
    filename = "distances.html"
    w = open( filename, "w" )     # opens the file for writing
    content='''<!DOCTYPE html><html lang="en"><head> <title>Bootstrap Example</title> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1"> <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css"> <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script> <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js"></script> <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js"></script></head><body><div class="container"><table class="table table-bordered"><thead><tr><th>Source</th><th>Destination</th><th>Distance</th><th> Duration </th></tr></thead>'''
    filename_to_read = "distances.json"
    f = open( filename_to_read, "r" )
    string_data = f.read()
    JD = json.loads( string_data )  # JD == "json dictionary"
    dst = JD["destination_addresses"]
    src = JD["origin_addresses"]
    sCt = 0 # I hate python w/o nice for loops x(
    dCt = 0
    errorMessage = "PATH DOES NOT EXIST"
    while sCt < len(src):
        info = JD["rows"][0]["elements"]
        # assumes that for origin addresses, there exists no repetition
        dCt = 0
        while dCt < len(dst):
            content += "<tr> <td>" + src[sCt]  +" </td><td>" + dst[dCt]  +" </td>"
            if info[dCt]["status"] == "OK":
                content += "<td>" + info[dCt]["distance"]["text"]  +" </td><td>" + info[dCt]["duration"]["text"]  +" </td>"
            else:
                content += "<td>DNE</td><td>DNE</td>"
            dCt += 1
            content += "</tr>"
        sCt += 1

    content_end = '''</table></div></body></html>'''
    w.write(content)
    w.write(content_end)                        # then, writes that string to a file
    w.close()                                   # and closes the file 
    print(os.getcwd() + filename)
    webbrowser.open("file://" + os.getcwd() + "/" + filename)

def main():
    """ top-level function for testing problem 1
    """

    Dests = ['Seattle,WA','Miami,FL','Boston,MA', 'San Francisco,CA', 'San Jose,CA']
    Sources = ['Claremont,CA','Seattle,WA','Philadelphia,PA', 'Mountain View,CA'] # ends
    addedNewData = False 
    if addedNewData:  # do we want to run the API call?
        google_api(Sources, Dests)  # get file
        # a lab key will be provided in class 
        # only use it as needed! (by setting the test to "if 0:")

    if 1:  # do we want to process the json file we've saved?
        json_process()
        createPage()

if __name__ == "__main__":
    main()

