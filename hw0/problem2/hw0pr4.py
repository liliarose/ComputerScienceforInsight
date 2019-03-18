# hw0pr2.py ~ phonebook analysis
# Name(s):
# be sure your file runs from this location, 
# at the level containing all of the "phonebook" directories

import os
import os.path
import shutil

def clean_digits(s):
    """ returns only the digits in the input string s """
    newS = ""
    for l in s:
        if l.isdigit():
            newS += l
    return newS

def getNumber(filename):
    """
        returns the phone # given a filename or -1 if it doesn't have one 
        assumes phone # on the first row and at least 7 digits
    """
    contents = open(filename, "r", encoding="latin1").read().rstrip().lstrip().split("\n")
    number = clean_digits(contents[0])
    if len(number) < 7:
        return "-1"
    return number

def getName(filename):
    """
        returns a list w/ last & first name 
        assumes name will be in the after & if last name first, have comma afterwards 
        ignores middle names & stuff in between 
    """
    contents = open(filename, "r", encoding="latin1").read().rstrip().lstrip().lower().split("\n")
    name = ["", ""]
    ct = 1
    while ct < len(contents):
        if not contents[ct].isspace():
            curr = contents[ct].split(" ")
            if "," in contents[ct]:
                name[0] = contents[ct][:len(curr[0])-1]
                name[1] = curr[-1]
            else:
                name[1] = curr[0]             
                name[0] = curr[-1]
            break
        ct += 1
    return name    

def writeCvs(cvsfile="phone.csv", path="."):
    """ 
        writes the contents of path in the file w/ the name [cvsfile]  
        assumes phone # on the first row and at least 7 digits --> if less, does not write it down.... 
    """
    AllFiles = list(os.walk(path))
    cvsContent = ""
    for item in AllFiles:
        foldername, LoDirs, LoFiles = item
        for filename in LoFiles:
            if filename[-3:] == "txt":
                fullfilename = foldername + "/" + filename
                number = getNumber(fullfilename)
                if number != "-1":
                    name = getName(fullfilename)
                    if name[0] == "":
                        print("WITHOUT NAME :|", fullfilename, name)
                    else:
                        cvsContent+= name[0] + ", " + name[1] + ", " + number + "\n"  
                else:
                    print( fullfilename, "w/o phone number:")
    cvs = open(cvsfile, 'w')
    cvs.write(cvsContent)

def sortByLastName(path="."):
    """ 
        returns a dictionary of lists containing the filename and full name (first & last) & number of each person
            (filename, first, last, number)
            assumes that every number has at least 7 digits
    """
    alpha ="abcdefghijklmnopqrstuvwxyz"
    sortedDict = {}
    for letter in alpha:
       sortedDict[letter] = []
    AllFiles = list(os.walk(path))
    for item in AllFiles:
        foldername, LoDirs, LoFiles = item
        for filename in LoFiles:
            if filename[-3:] == "txt":
                fullfilename = foldername + "/" + filename
                number = getNumber(fullfilename)
                if number != "-1":
                    name = getName(fullfilename)
                    sortedDict[name[0][0]].append((fullfilename, name[0], name[1], number))
                    # print(fullfilename, name, number)
    return sortedDict

def main():
    """ overall function that runs all examples """
    print("\nStart of main()")
    writeCvs() 
    dictLastName = sortByLastName()
    alpha ="abcdefghijklmnopqrstuvwxyz"
    for l in alpha:
        print("in", l + ", there exists", len(dictLastName[l]), "ppl")

    print("End of main()\n")

if __name__ == "__main__":
    main()


