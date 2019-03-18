import csv

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


data = readcsv("result.csv")
data2 = readcsv("result3.csv")

def differentiate(data, data2):
    for i in range(len(data)):
        if data[i][0] == data2[i][0]:
            print(i, "is same result")
        else:
            print("different:", data[i][1], data[i][2])
            print("\tscores", data[i][-1], data2[i][-1])
            print("\tresults:", data[i][0], data2[i][0])

differentiate(data, data2)

