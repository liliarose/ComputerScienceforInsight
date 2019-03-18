# hw0pr1.py

import time

def plus1(N):
    """ returns a number one larger than its input """
    return N+1

def countdown(N):
    """ counts downward from N to 0 printing only """
    for i in range(N,-1,-1):
        print("i ==", i)
        time.sleep(0.01)

def times42(s):
    """prints the string s 42 times (on separate lines) """
    for i in range(42):
        print(s)

def alien(N):
    """return the string "aliii...iiien" with exactly N "i"s """
    return ('al' + 'i'*N + 'en')

def count_digits(s):
    """ returns the number of digits in the input string s """
    count = 0
    for l in s:
        if l.isdigit():
            count += 1
    return count

def clean_digits(s):
    """ returns only the digits in the input string s """
    newS = ""
    for l in s:
        if l.isdigit():
            newS += l
    return newS

def clean_word(s):
    """returns an all-lowercase, all-letter version of the input string s"""
    s = s.lower()
    newS = ""
    for l in s:
        if l.isalpha():
            newS += l
    return newS

def main():
    """ main function for organizing -- and printing -- everything """
    print("\n\nStart of main()\n\n")
    # testing plus1
    result = plus1( 41 )
    print("plus1(41) returns", result)

    # testing countdown
    # print("Testing countdown(5):")
    # countdown(5)  # should print things -- with dramatic pauses!

    for i in range(10, 20, 2):
        print(plus1(i))
        print(alien(i))
    list1 = "For your choice of article (or both), problem 0 asks you to compose a one-paragraph reflection (4-5 sentences). Submit your reflection(s) in a file named hw0pr0.txt.".split(". ")
    for s in list1:
        print(s, ": ")
        print(count_digits(s))
        print(clean_digits(s))
        print(clean_word(s))

    print("\n\nEnd of main()\n\n")

if __name__ == "__main__":
    main()




