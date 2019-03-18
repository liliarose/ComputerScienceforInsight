#
# hw0pr2.py ~ phonebook analysis
#
# Name(s):
#

#
# be sure your file runs from this location, 
# at the level containing all of the "phonebook" directories
#
""" 
Across all of the files, how many of the phone numbers contain exactly 10 digits? 
Of these exactly-ten-digit phone numbers, how many are in the area code 909 (the area code will be the first three digits of a ten-digit number). 
How many people have the last name Davis?
Choose another name (with a less trivial answer): How many people have that last name?
How many people have the first name Davis? 
Choose another name (with a less trivial answer): How many people have that first name?
Are there any phone numbers that have more than 10 digits? 
"""
import os
import os.path
import shutil

def phoneNumbDigit(path, keyNum=10):
    """ returns the number of files w/ phone #s that have exactly keyNum digits across the current directory
        assumes that the phone # is on the first line
    """
    AllFiles = list(os.walk(path))
    count = 0
    for item in AllFiles:
        

def deepestDir(path):
    """return list of paths w/ the deepest directory?"""
    AllFiles = list(os.walk(path))
    maxCount = path.count("/")
    listOfDeepDir = [path]
    for item in AllFiles:
        foldername = item[0]
        #print(foldername)
        count = foldername.count('/')
        if count > maxCount:
           maxCount = count
           listOfDeepDir = [foldername]
           #print("current listOfDeepDir: ", listOfDeepDir)
        elif count == maxCount:
           listOfDeepDir.append(foldername)
           #print("current listOfDeepDir: ", listOfDeepDir)
    return listOfDeepDir

def maxFileDepth(path):
    """ returns the maximum depth of directories in the entire folder (in other words, what's the maximum number of times that it's possible to move deeper into a subdirectory, overall)
    does not include current directory"""
    AllFiles = list(os.walk(path))
    maxCount = 0
    for item in AllFiles:
      foldername, LoDirs, LoFiles = item 
      count = foldername.count('/')
      if count > maxCount:
         maxCount = count
    return maxCount

def how_many_txt_files(path):
    """ walks a whole directory structure
        and returns how many txt files are in it!
        call it with: how_many_txt_files(".")
        the (v1) (v2) etc. are different versions, to illustrate
        the process of _trying things out_ and _taking small steps_
    """
    # return 42  # just to check that it's working (v1)    
    AllFiles = list(os.walk(path))
    # print(AllFiles)    # just to check out what's up (v2)

    print("AllFiles has length: ", len(AllFiles), "\n")
    count2 = 0
    for item in AllFiles:
        # print("item is", item, "\n")    (v3)
        foldername, LoDirs, LoFiles = item   # cool!
        print("In", foldername, "there are", end=" ")
        count = 0
        for filename in LoFiles:
            if filename[-3:] == "txt":
                count += 1
        print(count, ".txt files found.")
        count2 += count
    return count2   # this is not _yet_ correct!



def main():
    """ overall function that runs all examples """

    print("Start of main()\n")

    num_txt_files = how_many_txt_files(".")
    print("num_txt_files in . is", num_txt_files)
    print("max_depth is ", maxFileDepth("."))
    print("End of main()\n")
    li = deepestDir(".")
    print("list of max_depth directories: ")
    for item in li:
        print(item)

if __name__ == "__main__":
    main()


