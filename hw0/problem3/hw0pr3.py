# hw0pr2.py ~ phonebook analysis
# Name(s):
#  (a) list the three questions you chose and (b) what the answers were
""" 
    1. count the number of times an ingredient appears 
    2. count the number of times a baking time appears 
    3. get the max baking time 
"""

import os
import os.path
import shutil

def findName(filename, key):
    """ 
        returns true/false if the key exists in the file
    """
    key = key.lstrip().rstrip().lower()
    f = open(filename, "r", encoding="latin1").read().lower()
    return (key in f)

def countInstruction(key="chop", path="."):
    """ returns # of times a word appears in the recipes """
    count = 0
    AllFiles = list(os.walk(path))
    for item in AllFiles:
        foldername, LoDirs, LoFiles = item
        for filename in LoFiles:
            if filename[-3:] == "txt":
               fullfilename = foldername + "/" + filename
               if findName(fullfilename, key): 
                count += 1
    return count

def isVegetarian(filename):
    """ returns True/False depending on whether a file is vege. or not """
    meatTypes = ["pork", "chicken", "beef"]
    for meat in meatTypes:
        if findName(filename, meat):
            return False
    return True

def getBakingTime(filename):
    """ 
        returns baking time in minutes --> assumes only hour & minute exist
        assumes that "Bake at 400 degrees for" _ [hours] _ [minutes] 
    """ 
    content = open(filename, "r", encoding="latin1").read().rstrip().lower().split("\n")
    bakeInfo = content[-1].lstrip().rstrip().split(" ")
    time = int(bakeInfo[-2])
    if "hour" in content[-1]:
        time += 60*int(bakeInfo[-4])
    return time 

def bakeTimeCount(path=".", key=90):
    count = 0
    AllFiles = list(os.walk(path))
    for item in AllFiles:
        foldername, LoDirs, LoFiles = item
        for filename in LoFiles:
            if filename[-3:] == "txt":
               fullfilename = foldername + "/" + filename
               if key == getBakingTime(fullfilename):
                count +=1
    return count

def getMaxBakeTime(path="."):
    maxC = ["filename", 0]
    AllFiles = list(os.walk(path))
    for item in AllFiles:
        foldername, LoDirs, LoFiles = item
        for filename in LoFiles:
            if filename[-3:] == "txt":
               fullfilename = foldername + "/" + filename
               tmp = getBakingTime(fullfilename) 
               if tmp > maxC[-1]:
                    maxC[0] = fullfilename
                    maxC[1] = tmp
    return maxC

def ingredientCount(key, path="."):
    count = 0
    AllFiles = list(os.walk(path))
    for item in AllFiles:
        foldername, LoDirs, LoFiles = item
        for filename in LoFiles:
            if filename[-3:] == "txt":
               fullfilename = foldername + "/" + filename
               if findName(fullfilename, key):
                count += 1
    return count

def pieRecipeSort(pathFrom=".", pathTo="."):
    """ 
        sorts the recipes under pathFrom into different directories under pathTo
        moves text files under recipes spot
        assumes that the files be labeled sweet/savory
    """
    # make the directories, if they exist, then pass 
    recipesPath = pathTo + "/recipes/"
    savoryPath = pathTo + "/recipes/savory_recipes/"
    sweetPath = pathTo + "/recipes/sweet_recipes/"
    vegetarianPath = pathTo + "/recipes/savory_recipes/vegetarian_recipes/"
    try:
        os.mkdir(recipesPath)
        os.mkdir(savoryPath)
        os.mkdir(sweetPath)
        os.mkdir(vegetarianPath)
    except OSError:
        pass

    AllFiles = list(os.walk(pathFrom))
    for item in AllFiles:
        foldername, LoDirs, LoFiles = item
        for filename in LoFiles:
            # checks to make sure it's a text file and is a pie recipe / has pie
            if filename[-3:] == "txt":
               fullfilename = foldername + "/" + filename
               if findName(fullfilename, "savory"):
                    if isVegetarian(fullfilename):
                        shutil.copyfile(fullfilename, vegetarianPath + filename)
                    else:
                        shutil.copyfile(fullfilename, savoryPath + filename)
               elif findName(fullfilename, "sweet"):
                    shutil.copyfile(fullfilename, sweetPath + filename)
               else:
                    shutil.copyfile(fullfilename, recipesPath + filename)

def printDirContents(path="."):
    """ prints contents under the current directory --> used to check stuff"""
    AllFiles = list(os.walk(path))
    for item in AllFiles:
        foldername, LoDirs, LoFiles = item
        print("\n" + foldername + ":")
        tmpStr = ""
        for filename in LoFiles:
            tmpStr += filename + " "
        print(tmpStr + "\n")

def checkingConditions(path="."):
    """ just checking if all recipes are actually pies & has savory or sweet--> and they all are in the current directory 
        walks a whole directory structure and returns how many txt files are in it! 
    """
    AllFiles = list(os.walk(path))
    count = [0, 0, 0, 0]

    for item in AllFiles:
        foldername, LoDirs, LoFiles = item  
        for filename in LoFiles:
            if filename[-3:] == "txt":
                count[0] += 1
                fullfilename = foldername + "/" + filename
                if findName(fullfilename, "pie"):
                    count[1] += 1
                if findName(fullfilename, "savory"):
                    count[2] += 1
                if findName(fullfilename, "sweet"):
                    count[3] += 1
    print(count[0], "?=", count[1], "?=", count[2], "+", count[3])   

def clean_digits(s):
    """ returns only the digits in the input string s """
    newS = ""
    for l in s:
        if l.isdigit():
            newS += l
    return newS

def currMostIngredient(filename, unit="kilogram"):
    """ 
        returns the ingredient and amount in the current file that is the most
        # assumes that for lines w/ ingredients, there exist no other number other than the ingredient amoutn 
        also assumes that the ingredient section and instruction section are labeled  
        assumes no new ingredients introduced after instruction is found
        assumes ingredients are listed in the following format: [#] [unit] of [ingredient]
    """
    result = ["ingredient", 0] # last # is the amount, I want to use structs ;( 
    unit = unit.lstrip().rstrip().lower()
    content = open(filename, "r", encoding="latin1").read().lstrip().rstrip().lower().split("\n")
    lineCount = 0
    lineLim = len(content)
    # first find where "ingredient" label is
    while lineCount < lineLim and not "ingredient" in content[lineCount]:
        lineCount += 1 
    lineCount += 1
    # stops when Instructions start
    while lineCount < lineLim and not "instruction" in content[lineCount]:
        if unit in content[lineCount]:
           line = content[lineCount].split(" ")
           amount = int(line[0].rstrip().lstrip())
           if amount > result[-1]:
                result[-1] = amount 
                nonIngre = len(line[0]) + len(line[1]) + len(line[2]) + 3 # + the 3 spaces
                result[0] = content[lineCount][nonIngre:]
        lineCount += 1
    return result

def mostIngredient(path=".", unit="kilogram"):
    """ returns a list w/ the fullfilename, ingredient, and amount 
        if more than one --> returns the first one that appears
    """ 
    # if this was c++, would use a struct & then make an array/vector of the most Ingredients.... ;(  
    mostIngredient = ["filename", "ingredient", 0] # last # is the amount """ 
    AllFiles = list(os.walk(path))
    for item in AllFiles:
        foldername, LoDirs, LoFiles = item
        for filename in LoFiles:
            if filename[-3:] == "txt":
               fullfilename = foldername + "/" + filename
               result = currMostIngredient(fullfilename, unit)
               #print(fullfilename + ":", result)
               if result[1] > mostIngredient[2]:
                    #print("changed")
                    mostIngredient[0] = fullfilename 
                    mostIngredient[1] = result[0]
                    mostIngredient[2] = result[1] 
    return mostIngredient 

def main():
    """ overall function that runs all examples """
    print("\nStart of main()")
    # checkingConditions()
    pieRecipeSort("allRecipes", ".")
    # printDirContents("recipes")
    #print(getBakingTime("recipes/sweet_recipes/recipe12.txt"))
    print("max baking time is", getMaxBakeTime())
    # print(currMostIngredient("recipes/sweet_recipes/recipe_for_disaster.txt"))
    print(bakeTimeCount("recipes"), "recipes have a 90 bake time")
    print("the final result: ", mostIngredient()) 
    print("the nutmeg appearence: ", ingredientCount("nutmeg"))
    print("End of main()\n")

if __name__ == "__main__":
    main()


