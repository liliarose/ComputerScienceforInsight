# hw0pr2.py ~ phonebook analysis
# Name(s):
# be sure your file runs from this location, 
# at the level containing all of the "phonebook" directories

# my questions:
# 1. if ordered by the first letter of their last name, which ones are in which?
    # returns a dictionary --> use sortByLastName() to evoke for current directory & sortByLastName("directory") for other cases 
""" 
result:
a: 333
b: 861
c: 605
d: 515
e: 209
f: 331
g: 496
h: 551
i: 58
j: 126
k: 513
l: 497
m: 836
n: 215
o: 147
p: 512
q: 37
r: 504
s: 1060
t: 376
u: 40
v: 214
w: 352
x: 2
y: 60
z: 102
    """
# 2. if "hashed" by their phone numbers by */% (ie. phone # = 1234--> "hash" = 1*2*3*4%36), how evenly distributed are the buckets? (what about other functions?)
    # call by hashTable([# of buckets])
"""
0 - 159
1 - 71
2 - 178
3 - 73
4 - 59
5 - 74
6 - 58
7 - 75
8 - 110
9 - 83
10 - 76
11 - 130
12 - 116
13 - 81
14 - 96
15 - 229
16 - 131
17 - 79
18 - 6947
19 - 52
20 - 58
21 - 134
22 - 116
23 - 97
24 - 265
"""
# 3. When phone digits multiplied, how many of them are multiples of 42?  
    # call by mFoldNumberCount([int/multiple to be counted]) 
# 8463 has a multiple of 42

import os
import os.path
import shutil
from collections import defaultdict

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

def getFirstName(filename):
    """
        returns a list w/ last & first name
        assumes name will be in the after & if last name first, have comma afterwards
        ignores middle names & stuff in between
    """
    contents = open(filename, "r", encoding="latin1").read().rstrip().lstrip().lower().split("\n")
    ct = 1
    while ct < len(contents):
        if not contents[ct].isspace():
            curr = contents[ct].split(" ")
            if "," in contents[ct]:
                return curr[-1]
            else:
                return curr[0]
        ct += 1

def getLastName(filename):
    """
        returns a list w/ last & first name
        assumes name will be in the after & if last name first, have comma afterwards
        ignores middle names & stuff in between
    """
    contents = open(filename, "r", encoding="latin1").read().rstrip().lstrip().lower().split("\n")
    name = ["last", "first"]
    ct = 1
    while ct < len(contents):
        if not contents[ct].isspace():
            curr = contents[ct].split(" ")
            if "," in contents[ct]:
                return contents[ct][:len(curr[0])-1]
            else:
                return curr[-1]
        ct += 1

def getName(filename):
    """
        returns a list w/ last & first name
        assumes name will be in the after & if last name first, have comma afterwards
        ignores middle names & stuff in between
    """
    contents = open(filename, "r", encoding="latin1").read().rstrip().lstrip().lower().split("\n")
    name = ["last", "first"]
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
                name = getName(fullfilename)
                if number != "-1":
                    sortedDict[name[0][0]].append((fullfilename, name[0], name[1], number))
                    # print(fullfilename, name, number)
    return sortedDict

def myHash(s, div):
    """ returns a integer 
        basically *the digits, | with another #
        and then %by div
    """
    largeInt = 1923829389210029381234893 
    ct = 1
    for i in s:
        ct *= int(i)
    ct = ct | largeInt
    return ct%div

def hashTable(div, path="."):
    """ returns a dictionary organized contents based on the hash fuction, not sure why I can't pass a function, but that's how this is going to end up being 
    can use list of list instead, but then would have to initialize up to div, so.... 
    """
    d = defaultdict(list)
    AllFiles = list(os.walk(path))
    for item in AllFiles:
        foldername, LoDirs, LoFiles = item
        for filename in LoFiles:
            if filename[-3:] == "txt":
                fullfilename = foldername + "/" + filename
                phone = getNumber(fullfilename)
                if phone != "-1":
                    d[myHash(phone, div)].append(fullfilename)  
    return d

def mFold(s):
    """ 
        returns the digits multiplied 
    """
    ct = 1
    for i in s:
        ct *= int(i)
    return ct

def mFoldNumberCount(key=42, path="."):
    ct = 0
    AllFiles = list(os.walk(path))
    for item in AllFiles:
        foldername, LoDirs, LoFiles = item
        for filename in LoFiles:
            if filename[-3:] == "txt":
                fullfilename = foldername + "/" + filename
                phone = getNumber(fullfilename)
                if phone != "-1" and mFold(phone)%key == 0:
                    ct +=1
    return ct
def how_many_txt_files(path):
    """ walks a whole directory structure and returns how many txt files are in it! """
    AllFiles = list(os.walk(path))
    count = 0
    for item in AllFiles:
        foldername, LoDirs, LoFiles = item  
        for filename in LoFiles:
            if filename[-3:] == "txt":
                count += 1
    return count   

def maxDepth(path):
    """ return max depth of directories in the entire folder
        does not count the current directory as the depth """
    AllFiles = list(os.walk(path))
    maxD = 0
    for item in AllFiles:
        depthCount = item[0].count("/") # item[0] == foldername
        if depthCount > maxD:
            maxD = depthCount
    return maxD

def maxDepthFolders(path):
    """ returns a list of the paths w/ the deepest directory """
    AllFiles = list(os.walk(path))
    maxDFolders = []
    maxD = 0
    for item in AllFiles:
        depthCount = item[0].count("/") # item[0] == foldername
        if depthCount > maxD:
            maxD = depthCount
            maxDFolders = [item[0]]
        elif depthCount == maxD:
            maxDFolders.append(item[0])
    return maxDFolders

def count_digits(s):
    """ returns the number of digits in the input string s """
    count = 0
    for l in s:
        if l.isdigit():
            count += 1
    return count

def getPhoneNumCount(filename):
    f = open(filename, "r", encoding="latin1")
    contents = f.read().split("\n")
    return count_digits(contents[0])

def phoneNumCountDigit(path, N=10):
    """ returns # of phone numbers contain exactly N digits across all of the files 
        assumes that phone # can only be on the first line """
    AllFiles = list(os.walk(path))
    count = 0
    for item in AllFiles:
        foldername, LoDirs, LoFiles = item
        for filename in LoFiles:
            if filename[-3:] == "txt":
                fullfilename = foldername + "/" + filename
                if getPhoneNumCount(fullfilename) == N:
                    count += 1
    return count 

def phoneNumCountMore(path, N=10):
    """ returns # of phone numbers contain more than N digits across all of the files
        assumes that phone # can only be on the first line """
    AllFiles = list(os.walk(path))
    count = 0
    for item in AllFiles:
        foldername, LoDirs, LoFiles = item
        for filename in LoFiles:
            if filename[-3:] == "txt":
                fullfilename = foldername + "/" + filename
                f = open(fullfilename, "r", encoding="latin1")
                contents = f.read().split("\n")
                if count_digits(contents[0]) > N:
                    count += 1
    return count

def checkAreaCodeSame(path, N=10, key="909"):
    """ returns # of phone #s that have 10 digits && area code == 909
         assumes that phone # can only be on the first line """
    AllFiles = list(os.walk(path))
    count = 0
    for item in AllFiles:
        foldername, LoDirs, LoFiles = item
        for filename in LoFiles:
            fullfilename = foldername + "/" + filename
            f = open(fullfilename, "r", encoding="latin1")
            contents = f.read().split("\n")
            phoneNumber = clean_digits(contents[0])
            if len(phoneNumber) == N and phoneNumber[0:3] == key:
                count+=1
                # print(fullfilename+":", contents[0])
    return count

def clean_word(s):
    """returns an all-lowercase, all-letter version of the input string s"""
    s = s.lower()
    newS = ""
    for l in s:
        if l.isalpha():
            newS += l
    return newS

def lastNameCount(path, key="Davis"):
    """ returns the # of ppl w/ the last name == key
        assumes name never on the second line 
        if last name is written first, assume always has a comma && 
        assumes last name has no non-alpha characters"""
    key = key.lstrip().rstrip().lower()
    AllFiles = list(os.walk(path))
    count = 0
    for item in AllFiles:
        foldername, LoDirs, LoFiles = item
        for filename in LoFiles:
            if filename[-3:] == "txt":
                fullfilename = foldername + "/" + filename
                contents = open(fullfilename, "r", encoding="latin1").read().split("\n")
                for i in range(1, len(contents)):
                # strips the content of the left and right whitespaces & then makes all characters to lowercase 
                    name = contents[i].lstrip().rstrip().lower()
                    if len(name) > len(key):
                        if ',' in name:
                            if name.startswith(key):
                                count += 1
                        elif name.endswith(key):
                            count += 1
                    # print(fullfilename +":", lastName)
    return count

def getFirstName(filename):
    """ 
    returns the first name 
    assumes name never on the second line 
    if last name is written first, assume always has a comma && the next name after that is the first name
    """
    contents = open(filename, "r", encoding="latin1").read().split("\n")
    for i in range(1, len(contents)):
        namec = contents[i].lstrip().rstrip().lower()
        if not namec.isspace():
            name = namec.split(" ")
            if "," in namec:
                return name[1].rstrip().lstrip()
            else: 
                return name[0].rstrip()
    return "Doesn't exist" 

def firstNameCount(path, key="Davis"):
    """ 
        returns the # of ppl w/ the first name == key
        assumes name never on the second line 
        if last name is written first, assume always has a comma && the next name after that is the first name
    """
    key = key.lstrip().rstrip().lower()
    AllFiles = list(os.walk(path))
    count = 0
    for item in AllFiles:
        foldername, LoDirs, LoFiles = item
        for filename in LoFiles:
            if filename[-3:] == "txt":
                fullfilename = foldername + "/" + filename
                if key == getFirstName(fullfilename):
                    count += 1
    return count 

def main():
    """ overall function that runs all examples """
    print("\nStart of main()")
    """"
    num_txt_files = how_many_txt_files(".")
    print("num_txt_files in is", num_txt_files)
    print("maxDepth is", maxDepth("."))
    print("maxDepthFolders are") 
    list = maxDepthFolders(".")
    for f in list:
        print(f)
    print("phone # w/ 10 digits is", phoneNumCountDigit("."))
    # print("phone # w/ 9 digits is", phoneNumCountDigit(".", 9))
    print("phone # w/ 10 digits & has areacode == 909 is", checkAreaCodeSame("."))
    print("phone # w/ 10 digits & has areacode == 408 is", checkAreaCodeSame(".", 10, "408")) 
    print("# of ppl w/ the last name Davis: ", lastNameCount("."))
    print("# of ppl w/ the last name Johnson: ", lastNameCount(".", "Johnson"))
    print("# of ppl w/ the first name Davis: ", firstNameCount("."))
    print("# of ppl w/ the first name Kenda: ", firstNameCount(".", "Kenda"))
    print("phone # w/ > 10 digits:", phoneNumCountMore("."))
    dictLastName = sortByLastName()
    alpha ="abcdefghijklmnopqrstuvwxyz"
    for l in alpha:
        print(l+":", len(dictLastName[l]))
    d = hashTable(25)
    for i in range(25):
        print(i, "-", len(d[i]))
    """
    # print(mFoldNumberCount(), "has a multiple of 42")
    print("End of main()\n")

if __name__ == "__main__":
    main()


