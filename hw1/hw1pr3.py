import wikipedia 
# https://pypi.org/project/wikipedia/
# run pip install wikipedia if it isn't installed/downloaded 
# question: 
# is there any correlation with the length of a book's summary or content from wikipedia and a book's rating
# btw, running this is super slow...(at least for the good reads api)

from goodreads import client
# ruby api: https://www.goodreads.com/api/index#search.books
# python api: https://github.com/sefakilic/goodreads

import json
import math 
from collections import defaultdict

# the number of books used for this test 
booksCount = 100

def getBookInfo(count=booksCount):
    """
    returns a list of objects, books(going by id) --> all books that exist from #1 to count (inclusive 
    """
    gc = client.GoodreadsClient("JdH0YOXuBLIFXhXUGMNmA", "XtIlhsavfhSICDEMLzWLRyKp509VNaeGbVUh7tJaQ")
    gc.authenticate("JdH0YOXuBLIFXhXUGMNmA", "XtIlhsavfhSICDEMLzWLRyKp509VNaeGbVUh7tJaQ")
    bookList = []

    for i in range(1, count+1):
        try:
            bookList.append(gc.book(i)) # get id --> .gid
            print('#' + bookList[-1].gid, bookList[-1].title)
        except Exception:
            print("book", i, "cannot be found?") 
    return bookList  

def getWikiInfo(bookList):
    """
    from a list of books, get the length of the book's summary 
    """
    wikiInfo = defaultdict(int)
    for book in bookList:
        try:
            tmp = book.title.find(')')
            if tmp != -1:
                wikiInfo[book.title] = len(wikipedia.summary(book.title))
            else:
                wikiInfo[book.title] = len(wikipedia.summary(book.title[:tmp]))
            print(wikiInfo[book.title])
        except Exception:
            print("name not specific enough or there exists none?")
            print(book.title + ":\n", wikipedia.search(book.title))
    return wikiInfo

def process(booklist, contentLength):
    """
    processes the list & uses a dictionary to keep count of all the different wikiInfo/book rating 
    returns a tuple of elements and dictionary 
    """
    lElem = []
    distrib = defaultdict(int)
    for book in booklist:
        if book.average_rating != 0: 
            tmp = round(wikiInfo[book.title]/float(book.average_rating))
            if not tmp in lElem:
                lElem.append(tmp) 
            distrib[tmp] += 1
    return (lElem, distrib)

def redistrub(origDistrib, factor):
    """
        input: tuple of elements and dictionary,
               factor = # to divide the bins by
        output: redistributed tuple of elements and dictionary 
    """
    newdistrib = defaultdict(int)
    lElem = []
    for i in origDistrib[0]:
        tmp = round(i/factor)
        if not tmp in lElem:
            lElem.append(tmp)
        newdistrib[tmp] += origDistrib[1][i]
    return (lElem, newdistrib)

def main():
    bookList = getBookInfo()
    wikiInfo = getWikiInfo(bookList)
    result = process(bookList, wikiInfo)
    print(result)
    print(redistrub(result, 100))

if __name__ == "__main__":
    # main()
    bookList = getBookInfo()
    wikiInfo = getWikiInfo(bookList)
    result = process(bookList, wikiInfo)
    print(result[1])
    print("redistributed:", redistrub(result, 50)[1])


