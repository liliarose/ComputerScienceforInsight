# starter file for hw1pr2, cs35 spring 2017...
import webbrowser, os
import csv
# readcsv is a starting point - it returns the rows from a standard csv file...
from collections import defaultdict
def readcsv(csv_file_name):
    """ readcsv takes as
         + input:  csv_file_name, the name of a csv file
        and returns
         + output: a list of lists, each inner list is one row of the csv
           all data items are strings; empty cells are empty strings
        in this format: 
           [ item1, item2...]
    """
    try:
        csvfile = open( csv_file_name, newline='' )  # open for reading
        csvrows = csv.reader( csvfile )              # creates a csvrows object
        all_rows = []                               # we need to read the csv file
        for row in csvrows:                         # into our own Python data structure
            all_rows.append(row)                    # adds only the word to our list
        del csvrows                                  # acknowledge csvrows is gone!
        csvfile.close()                              # and close the file
        return all_rows                              # return the list of lists

    except FileNotFoundError as e:
        print("File not found: ", e)
        return []
""""
def dictToList(d, key="abcdefghijklmnopqrstuvwxyz0123456789"):
    newList = []
    for k in key:
        newList.append((k, d[k]))
    return newList
"""

# write_to_csv shows how to write that format from a list of rows...
#  + try write_to_csv( [['a', 1 ], ['b', 2]], "smallfile.csv" )
def write_to_csv(d, filename, keys="abcdefghijklmnopqrstuvwxyz0123456789"):
    """ readcsv takes as
         + input:  csv_file_name, the name of a csv file
        and returns
         + output: a list of lists, each inner list is one row of the csv
           all data items are strings; empty cells are empty strings
    """
    try:
        csvfile = open( filename, "w", newline='' )
        filewriter = csv.writer( csvfile, delimiter=",")
        if type(d) == list:
            for row in d:
                filewriter.writerow(row)
        else:
            for key in keys:
                filewriter.writerow([key, d[key]])
        csvfile.close()
    except Exception as e:
        print(e)
        print("File", filename, "could not be opened for writing...")

# csv_to_html_table_starter
#   Shows off how to create an html-formatted string
#   Some newlines are added for human-readability...

def firstLetterCount(row):
    """ gets a row & returns the first letter and relative frequency as a tuple """
    first_letter = str(row[0]).lower()[0]
    num  = float(row[1])
    return(first_letter, num)

def lastLetterCount(row):
    """ gets a row & returns the last letter and relative frequency as a tuple """
    last_letter= str(row[0]).lower()[-1]
    num  = float(row[1])
    return(last_letter, num)

def secondLetterCount(row):
    """ gets a row & returns the second letter and relative frequency as a tuple"""
    try:
        return (str(row[0]).lower()[1], float(row[1]))
    except Exception as e:
        return ("NULL", float(row[1]))

def count(filename, func):
    """ returns a dictionary (defaultdict) of
        weighted first-letter (case-insensitive) counts from
        the file wds.csv
    """
    LoR = readcsv(filename)
    # print("LoR is", LoR)
    counts = defaultdict(int)
    for Row in LoR:
        info = func(Row) # format returned --> (key, amount to add)
        counts[info[0]] += info[1]   # add one to that letter's counts
    # done with for loop
    # print(counts)
    return counts

def createPage(readFile, writeFile, tableTitle=["key", "frequency"]):
    """ input: the newly written file 
            the file name to be written
            the tableTitle (in case there are cases were it's not just key & frequency)
        creates a new html page & creates a table with bootstrap
        also opens it? (testing?) 
    """
    # header 
    content='''<!DOCTYPE html><html lang="en"><head> <title>Bootstrap Example</title> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1"> <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css"> <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script> <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js"></script> <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js"></script></head><body><div class="container"><table class="table table-bordered"> <thead><tr>'''
    data = readcsv(readFile)
    try:
        w = open(writeFile, "w")
        # create table headers 
        for title in tableTitle:
            content += '<th>' + title +'</th>'
        content += '</tr></thead>'
        # assumes table to be list of list 
        for li in data:
            content += '<tr>'
            for info in li:
                content += '<td>' + info + '</td>'
            content += '</tr>'
        content_end = '''</table></div></body></html>'''
        w.write(content)
        w.write(content_end)                        # then, writes that string to a file
        w.close()                                   # and closes the file
        print("wrote in file", os.getcwd() +"/" +  writeFile)
        webbrowser.open("file://" + os.getcwd() + "/" + writeFile)
    except FileNotFoundError as e: 
        print(writeFile, "cannot be found")
    except Exception as e:
        print(e)

def printAlphaDict(dictionary):
    """ prints the elements of a (default) dictionary --> alpha + num & assumes all lowercase keys"""
    s = "abcdefghijklmnopqrstuvwxyz0123456789"
    for c in s:
        print(c, dictionary[c])

def main():
    """ run this file as a script """
    LoL = readcsv( "wds.csv" )
    # print(LoL[:10])
    # test writing
    write_to_csv(LoL[:10], "tenrows.csv")
    # print("first letter count:")
    # printAlphaDict(count("tenrows.csv", firstLetterCount))
    # print("\nlast letter count:") 
    # printAlphaDict(count("tenrows.csv", lastLetterCount))
    # print("\nsecond letter count:")
    # printAlphaDict(count("tenrows.csv", secondLetterCount))
    # csv_to_html_table_starter(LoL)
    # output_html = csv_to_html_table_starter( LoL[:10] )
    # print("output_html is", output_html)
    llc = count("tenrows.csv", lastLetterCount)
    slc = count("tenrows.csv", secondLetterCount)
    # print(llc)
    # print(slc)
    write_to_csv(llc, "frequencies1.csv")
    write_to_csv(slc, "frequencies2.csv")
    createPage("frequencies1.csv", "frequencies1.html", ["key", "last letter frequency"])
    createPage("frequencies2.csv", "frequencies2.html", ["key", "second letter frequency"])

if __name__ == "__main__":
    main()
