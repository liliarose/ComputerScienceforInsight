#
# hw3pr2.py 
#
# Person or machine?  The rps-string challenge...
#
# This file should include your code for 
#   + extract_features( rps ),               returning a dictionary of features from an input rps string
#   + score_features( dict_of_features ),    returning a score (or scores) based on that dictionary
#   + read_data( filename="rps.csv" ),       returning the list of datarows in rps.csv
#
# Be sure to include a short description of your algorithm in the triple-quoted string below.
# Also, be sure to include your final scores for each string in the rps.csv file you include,
#   either by writing a new file out or by pasting your results into the existing file
#   And, include your assessment as to whether each string was human-created or machine-created
# 
#



"""
Short description of (1) the features you compute for each rps-string and 
      (2) how you score those features and how those scores relate to "humanness" or "machineness"
      
      Scoring humanness -->
        higher score = human
        lower score = machine

      I used the longest repeating substring algorithm and also partially dependent on the amount of times a letter appears 
      consecutively (and the # of times it appears)
      I fiddled with the numbers a lot and used a 500 length array as the basis (low end) and made sure it was below

      for lrsubstring: scores[i] += math.sqrt(len(subStrings[i][j][0]) * (subStrings[i][j][1])**2)
        + scores[i] *500 --> int 
      for consecutive --> round(math.sqrt(c**2 + currMaxL**2))//10 for all 3 letters 
"""


# Here's how to machine-generate an rps string.
# You can create your own human-generated ones!

import random
import csv 
import re 
import math

def gen_rps_string(num_characters):
    """ return a uniformly random rps string with num_characters characters """
    result = ''
    for i in range( num_characters ):
        result += random.choice( 'rps' )
    return result

# Here are two example machine-generated strings:
rps_machine = [gen_rps_string(200) for i in range(500)]
# rps_machine1 = gen_rps_string(200)
# rps_machine2 = gen_rps_string(200)
# print those, if you like, to see what they are...

# from geeksforgeeks, didn't have enough t

def longestRepeatedSubstring(str):
    """
        algorithm for the longest repeated substring
    """
    n = len(str)
    LCSRe = [[0 for x in range(n + 1)] for y in range(n + 1)]
    res = "" # To store result
    res_length = 0 # To store length of result
    index = 0
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if (str[i - 1] == str[j - 1] and
                LCSRe[i - 1][j - 1] < (j - i)):
                LCSRe[i][j] = LCSRe[i - 1][j - 1] + 1
                if (LCSRe[i][j] > res_length):
                    res_length = LCSRe[i][j]
                    index = max(i, index)
            else:
                LCSRe[i][j] = 0
    if (res_length > 0):
        for i in range(index - res_length + 1, index + 1):
            res = res + str[i - 1]
    return res

from collections import defaultdict

def mRSinLRS(string, lLim=4, cLim=2):
    """
        dependent on the longest substring function & gets 3 inputs (only 1 needed):
        string --> string to be processed 
        this function finds the greatest repeated substring of a substring until there only exists it is less than the length lLim 
        then it returns that substring and # of times it occurred in the string unless the # of times it appears is less than cLim 
    """
    substring = string
    cString = string
    while len(substring) > lLim: 
        cString = substring
        substring = longestRepeatedSubstring(cString)
    if(string.count(cString) > cLim):
        return (cString, string.count(cString))
    return False

def longestConsecutive(s, alpha='rps', cLim = 1, mLim=25):
    """
        finds the longest consecutive of each letter & then calculates the score by # number of times it appears 
    """
    maxL = [0]* len(alpha)
    totMax = 0
    for l in range(len(alpha)):
        currMaxL = 0
        for i in range(1, len(s)):
            if s[i] == alpha[l]:
                currMaxL += 1
            else:
                c = s.count(alpha[l]*currMaxL)
                test = round(math.sqrt(c**2 + currMaxL**2))
                if currMaxL > cLim and currMaxL > maxL[l] and test > mLim:
                    maxL[l] = c*currMaxL
                currMaxL = 0
        totMax += maxL[l]*maxL[l]
    return totMax//10

def score_find(data, times=1):
    # input: just the strings themselves & the number of times mRSinLRS should be found 
    # outputs the score based on mRSinLRS & longestConsecutive 
    scores = [0] * len(data)
    subStrings = [[None] for i in range(len(data))] 
    #print(subStrings) 
    for i in range(len(data)):
        cString = data[i]
        for j in range(times):
            try:
                t = mRSinLRS(cString, 4, 4)
                if j == 0:
                    subStrings[i] = [t]
                else:
                    subStrings[i].append(t)
                if subStrings[i][j]:
                    scores[i] += math.sqrt(len(subStrings[i][j][0]) * (subStrings[i][j][1])**2)
                    cString = re.sub(subStrings[i][j][0], 'y', cString)
            except TypeError:
                print("type error:", subStrings[i], t, scores[i], cString)
        # print(scores[i]*50)
        tmp = scores[i]*100 
        scores[i] = int(scores[i]*100) + (longestConsecutive(data[i]))
        if not (int(tmp) -scores[i] == 0):
            print (scores[i], tmp)
    return scores 
    # (scores, subStrings)

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

def write_to_csv(filename, d):
    """ readcsv takes as
         + input:  csv_file_name, the name of a csv file
        and returns
         + output: a list of lists, each inner list is one row of the csv
           all data items are strings; empty cells are empty strings
    """
    try:
        csvfile = open( filename, "w", newline='' )
        filewriter = csv.writer( csvfile, delimiter=",")
        for row in d:
            filewriter.writerow(row)
        csvfile.close()
    except Exception as e:
        print(e)
        print("File", filename, "could not be opened for writing...")
#
# you'll use these three functions to score each rps string and then
#    determine if it was human-generated or machine-generated 
#    (they're half and half with one mystery string)
#
# Be sure to include your scores and your human/machine decision in the rps.csv file!
#    And include the file in your hw3.zip archive (with the other rows that are already there)
#

def calcMach(scores, cutoff):
    machine = 0
    #machine = [""] * len(scores)
    for i in range(len(scores)):
        if scores[i] > cutoff:
            machine += 1
    return machine

def calcMachArr(scores, cutoff):
    machine = [""] * len(scores)
    for i in range(len(scores)):
        if scores[i] > cutoff:
            machine[i] = 'h'
        else:
            machine[i] = 'm'
    return machine

def calcDist(scores):
    dist = defaultdict(int)
    for score in scores:
        dist[score] += 1
    return dist


times = 5

data = readcsv("cs35rps.csv")
actualData = [data[i][2] for i in range(len(data))]
# print(actualData)

scores = score_find(actualData, times)
scores2 = sorted(scores)
print("my generated strings:")
print((score_find(mygenerated, times)))
print("finding machine generated stuff")
scores3 = score_find(rps_machine, times)
scores4 = sorted(scores3)
result2 = [ [ rps_machine[i], scores3[i] ] for i in range(len(scores3))]
print(scores4)
write_to_csv("result2.csv", result2)
breakPt = round(scores2[(len(scores2))//2]/10)*10
#/10)*10 # round(scores4[-2]/10)*10 #scoresround(scores[len(scores)//2+1]/10)*10
mvh = calcMachArr(scores, breakPt)
result = [[mvh[i], data[i][1], data[i][2], scores[i] ] for i in range(len(scores))]
print(scores2, breakPt)
print(calcMach(scores2, breakPt))
write_to_csv("result.csv", result)

def batch_rps(rps1, rps2):
    rps1 = rps1.lower()
    rps2 = rps2.lower()
    result = defaultdict(int)
    lim = min(len(rps1), len(rps2))
    for i in range(lim):
        if rps1[i] == rps2[i]:
            result["ties"] += 1
        elif rps1[i] > rps2[i] or (rps1[i] == 'p' and rps2[i] == 'r'):
            result["rps1wins"] += 1
        else:
            result["rps2wins"] += 1
    return result
"""
player1 = "rrrrrrpppppppppppprrrrrr"
player2 = "pppppppppppprrrrrr"

print(batch_rps(player1, player2))
"""
    


