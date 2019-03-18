import csv
from collections import defaultdict
import os, webbrowser
import re 
# readcsv is a starting point - it returns the rows from a standard csv file...
#
def readcsv( csv_file_name ):
    """ readcsv takes as
         + input:  csv_file_name, the name of a csv file
         + output: a list of lists, each inner list is one row of the csv
           all data items are strings; empty cells are empty strings
    """
    try:
        csvfile = open( csv_file_name, newline='' )  # open for reading
        csvrows = csv.reader( csvfile )              # creates a csvrows object
        all_rows = []                              # we need to read the csv file
        for row in csvrows:                         # into our own Python data structure
            all_rows.append( row )                  # adds only the word to our list
        del csvrows                                  # acknowledge csvrows is gone!
        csvfile.close()                              # and close the file
        return all_rows                              # return the list of lists
    except FileNotFoundError as e:
        print("File not found: ", e)
        return []

def readcsv2(csv_file_name):
    """ readcsv takes as
         + input:  csv_file_name, the name of a csv file (assumes there exists only 2 elements per row
         + output: a default string dictionary 
    """
    try:
        csvfile = open( csv_file_name, newline='' )  # open for reading
        csvrows = csv.reader( csvfile )              # creates a csvrows object

        all_rows = {}  
        for row in csvrows:                         # into our own Python data structure
            try:
                all_rows[row[0]] = row[1]
            except:
                print(row)
        del csvrows                                  # acknowledge csvrows is gone!
        csvfile.close()                              # and close the file
        return all_rows                              # return the list of lists
    except FileNotFoundError as e:
        print("File not found: ", e)
        return {} 

def annotate_text(text, annotations, specialize=["Shakespeare Substitutions", "Hamlet, Act 1, Scene 4"]):
        """ input: the original text, the annotations & 
               an optional list of strings for the website title & text title 
        output: changes the '\n' characters to "<br>" & uses the annotations dictionary
        """
        # style variables 
        textColor = 'skyblue' 
        textShadow = '.5'
        start='<!DOCTYPE html><html lang="en"><head> <title>' + specialize[0] + '</title> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1"> <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css"> <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script> <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script> <style>.popoverStuff{color:' + textColor + '; font-weight: bold; text-shadow:' + textShadow + 'px' + textShadow + 'px;}</style></head><body><div class="container"><h2>' + specialize[1] + '</h2> <br>' 
        end = '''</div><script>$(document).ready(function(){$('[data-toggle="popover"]').popover();});</script></body></html>'''
        content = '<h3>Original:</h3><p>' + re.sub("\n","<br>", text) + '</p><br>'# split by line
        content += '<h3>Annotated:</h3><p>'
        text = text.split("\n")
        for line in text:
            line = line.split(" ")
            for word in line:
                wordStrip = re.sub(r'\W+', '', word).lower()
                if wordStrip in annotations: 
                    content += '<a href="#" data-toggle="popover" data-trigger="hover" data-content="' + annotations[wordStrip] + '"class="popoverStuff">' + word + ' </a>' 
                else:
                    content += word + " "
            content += "<br>"
        content += '</p>'
        return start + content + end

def saveFile(filename, content):
    """ 
        writes content into a file w/ filename
    """
    f = open(filename, "w" )    
    f.write(content)    
    f.close() 

HAMLET_A1S4 = """
The king doth wake tonight and takes his rouse,
Keeps wassail and the swaggering upspring reels,
And, as he drains his draughts of Rhenish down,
The kettle-drum and trumpet thus bray out
The triumph of his pledge.
"""
HAMLET_SUBS = { "doth":"does", "rouse":"partying",
                "wassail":"drinks",
                "reels":"dances", "rhenish":"wine",
                "bray":"blare", "pledge":"participation"}


def main():
    """ running this file as a script """
    # uncomment this to test 
    """
    html = annotate_text(HAMLET_A1S4, HAMLET_SUBS)
    filename = "hamlet1_4.html"
    saveFile(filename, html)
    print("created", filename)
    webbrowser.open("file://" + os.getcwd() + '/' + filename)
    """
    # my files 
    # src: http://www.shanleyworld.com/ShanleyWorld/Shakespeare_files/Elizabethan%20English%20and%20Shakespearean%20Vocabulary.pdf + sparknotes & google search
    annotations = readcsv2("test.txt") 
    henryV_chorus = open("henryV_act1.txt", 'r').read()
    html = annotate_text(henryV_chorus, annotations, ["Shakespeare Substitutions", "Henry V Act 1"])
    filename2 = 'henryVact1.html'
    saveFile(filename2, html)
    print("created", filename2)
    webbrowser.open("file://" + os.getcwd() + '/' + filename2)
    
    henryV= open("henryVChorus.txt", 'r').read()
    html = annotate_text(henryV_chorus, annotations, ["Shakespeare Substitutions", "Henry V Chorus"])
    filename2 = 'henryVChorus.html'
    saveFile(filename2, html)
    print("created", filename2)
    webbrowser.open("file://" + os.getcwd() + '/' + filename2)

if __name__ == "__main__":
    main()


