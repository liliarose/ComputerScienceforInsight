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
      because 
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

def mRSinLRS(string):
    substring = string
    cString = string
    while len(substring) > 1:
        cString = substring
        substring = longestRepeatedSubstring(cString)
    if(string.count(cString) > 1):
        return (cString, string.count(cString))
    return False

def score_find(data, times=1):
    # input: just the strings themselves & the number of times mRSinLRS should be found 
    
    scores = [0] * len(data)
    subStrings = [[0] for i in range(len(data))] 
    print(subStrings) 
    for i in range(len(data)):
        cString = data[i]
        for j in range(times):
            if j != 0 and len(subStrings) == j and subStrings[i][j-1][1]>1:
                t = mRSinLRS(cString)
                if t: 
                    subStrings[i].append(mRSinLRS(cString))
                    scores[i] += subStrings[i][j][0] * subStrings[i][j][1]
                    cString = re.sub(subStrings[i][j][0], 'y', cString)
        print(scores[i])
    return scores 
    # (scores, subStrings)

"""
def removeLRS(data):
    listOfLRS = [0] * len(data)
    data2 = [0] * len(data)
    flag = 0
    for i in range(len(data)):
        cLRS = longestRepeatedSubstring(data[i])
        listOfLRS[i] = [(cLRS, data[i].count(cLRS))]
        # print(cLRS)
        if len(cLRS) > 2:
            data2[i] = re.sub(cLRS, '', data[i])
        else:
            flag +=1
        
    while flag < len(data2):
        for i in range(len(data2)):
            if len(listOfLRS[i][-1][0]) > 2:
                cLRS = longestRepeatedSubstring(data2[i])
                listOfLRS[i].append((cLRS, data2[i].count(cLRS))) #(cLRS, data2[i].count(cLRS)))
                # print(cLRS)
                if(len(cLRS) > 2):
                    data2[i] = re.sub(cLRS, '', data2[i])
                else:
                    flag += 1
        print("flag:", flag)
    return (listOfLRS, data2)
"""
"""
def removeLRS(data, time = 10):
    listOfLRS = [0] * len(data)
    data2 = [0] * len(data)
    for i in range(len(data)):
        cLRS = longestRepeatedSubstring(data[i])
        listOfLRS[i] = [(cLRS, data[i].count(cLRS))]
        data2[i] = re.sub(cLRS, '', data[i])
    for j in range(time):
        for i in range(len(data2)):
            if len(listOfLRS[i][-1][0]) > 2:
                cLRS = longestRepeatedSubstring(data2[i])
                listOfLRS[i].append((cLRS, data2[i].count(cLRS))) #(cLRS, data2[i].count(cLRS)))
                #print(listOfLRS[i])
                if(len(cLRS) > 2):
                    data2[i] = re.sub(cLRS, '', data2[i])
        print(j)
    return (listOfLRS, data2)
def score_features(data1, data2):
    score = [0] * len(data1)
    for i in range(len(data1)):
        score[i] = (len(data1[2]) - len(data2[1][i])) #  + len(data2[0][i]))/len(data1[2]), 2)
    return score   # return a humanness or machineness score

def score_features2(data1, data2):
    patternLengths = [0] * len(data2[0])
    for i in range(len(data2[0])):
        for s in data2[0][i]:
            patternLengths[i] += len(s)
    score = [0] * len(data1)
    for i in range(len(data1)):
        score[i] = (len(data1[2]) - len(data2[1][i]) - patternLengths[i])
    return score

def score_features4(data1, data2):
    score = [0] * len(data1)
    for i in range(len(data1)):
        for s in data2[0][i]:
            score[i] += len(s[0])* (s[1]**2)
    return score

def editDistDP(str1, str2, m, n): 
    dp = [[0 for x in range(n+1)] for x in range(m+1)] 
    for i in range(m+1): 
        for j in range(n+1): 
            if i == 0: 
                dp[i][j] = j    # Min. operations = j 
            elif j == 0: 
                dp[i][j] = i    # Min. operations = i 
            elif str1[i-1] == str2[j-1]: 
                dp[i][j] = dp[i-1][j-1] 
            else: 
                dp[i][j] = 1 + min(dp[i][j-1],  dp[i-1][j], dp[i-1][j-1])    # Replace 
    return dp[m][n] 

def score_features4(data1, data2, )

def score_features3(data1, data2, times=5, times2=3):
    scoreT = [[0] for i in data1] 
    for i in range(len(data2[0])):
     for j in range(max(min(len(data2[0][i])-1, times), 0)):
      for k in range(j+1, min(len(data2[0][i]), times)):
       x = editDistDP(data2[0][i][j][0], data2[0][i][k][0], len(data2[0][i][j][0]), len(data2[0][i][k][0]))
       # data2[0][i][k][1]
       #print(i, ": ", x, type(x), data2[0][i][k][1], type(data2[0][i][k][1]))
       scoreT[i].append(pow(x, data2[0][i][k][1]/10))
       #score[i] += editDistDP(data2[0][i][j][0], data2[0][i][k][0], len(data2[0][i][j][0]), len(data2[0][i][k][0]))*data2[0][i][k][1]
    #print(scoreT)
    score = [0] * len(data1)
    for i in range(len(data2[0])):
        for j in range(times):
            if len(scoreT[i]) > 0:
                t = max(scoreT[i])
                #print(score[i])
                score[i] += t #(times2-j)*(times2-j(times2-j))
                scoreT[i].remove(t)
        score[i] = int(score[i]*(10**1)) 
        print(score[i])
    return score 
"""

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
    for score in scores:
        if score > cutoff:
            machine += 1
    return machine

def calcDist(scores):
    dist = defaultdict(int)
    for score in scores:
        dist[score] += 1
    return dist

data = readcsv("cs35rps.csv")
actualData = [data[i][2] for i in range(len(data))]
"""
times = 10  
data2 = removeLRS(actualData)
scores = score_features3(actualData, data2)
maxTimes = [0] * len(scores)
for i in range(len(scores)):
    for j in range(len(data2[0][i])):
        if data2[0][i][j][1] > maxTimes[i]:
            maxTimes[i] = data2[0][i][j][1]
result = [[data[i][2], data2[1][i], maxTimes[i], scores[i] ] for i in range(len(scores))]
# result = [ [data[i][0], data[i][2], data2[1][i], len(data2[1][i]), scores[i] ] for i in range(len(data2[1]))]

print(calcDist(scores))

tmp = removeLRS(rps_machine)
scores = score_features3(rps_machine, tmp)
result2 = [ [ rps_machine[i], scores[i] ] for i in range(len(scores))]
calc = calcMach(scores, 200)
print(calcDist(scores))
print(calc, len(scores) - calc)
"""
times = 1
scores = score_find(actualData, 3)
# scores = data2[0]
# print(scores)
result = [[data[i][2], scores[i] ] for i in range(len(scores))]

scores = score_find(rps_machine)
# scores = tmp[0]
# print(scores)
result2 = [ [ rps_machine[i], scores[i] ] for i in range(len(scores))]

write_to_csv("result.csv", result)
write_to_csv("result2.csv", result2)

