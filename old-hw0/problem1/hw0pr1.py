#
# hw0pr1.py
#

# An example function
#

def alien(N):
 """return the string "aliii...iiien" with exactly N "i"s"""
 s = "al"
 for i in range(N):
  s+= 'i'
 s += 'en'
 return s

def clean_digits(s):    
  """returns only the digits in the input string s"""
  new_str = ""
  digits = "0123456789"
  for l in s:
    if l in digits:
      new_str += l
  return new_str

def clean_word(s):    
  """returns an all-lowercase, all-letter version of the input string s
     assuming letter means only abcd...."""
  if not s.islower(): 
    s = s.lower()
  new_str = ""
  abc = "abcdefghijklmnopqrstuvwxyz"
  for l in s:
    if l in abc:
      new_str += l
  return new_str

def count_digits(s):
 """returns the number of digits in the input string s"""
 digits = "0123456789"
 count = 0 
 for l in s:
  if l in digits:
   count+=1
 return count

def times42(s):
    """ print the string s 42 times (on separate lines)"""
    for i in range(42):
        print(s)

def plus1( N ):
    """ returns a number one larger than its input """
    return N+1

# An example loop - with a countdown being printed
#
import time

def countdown( N ):
    """ counts downward from N to 0 printing only """
    for i in range(N,-1,-1):
        print("i ==", i)
        time.sleep(0.01)

# An example main() function - to keep everything organized!
#
def main():
    """ main function for organizing -- and printing -- everything """
    print("\n\nStart of main()\n\n")
    list1 = "For your choice of article (or both), problem 0 asks you to compose a one-paragraph reflection (4-5 sentences). Submit your reflection(s) in a file named hw0pr0.txt.".split(". ")
    for i in range(10, 20):
      print(alien(i))
      print(plus1(i))
      #print(times42(i))
    for s in list1:
      print(s, ": ")
      print(count_digits(s))
      print(clean_digits(s))
      print(clean_word(s))
    print("\n\nEnd of main()\n\n")

# This conditional will run main() when this file is executed:
#
if __name__ == "__main__":
    main()



# ++ The challenges:  Create and test as many of these five functions as you can.
#
# The final three may be helpful later...
#
# times42( s ):      which should print the string s 42 times (on separate lines)
# alien( N ):          should return the string "aliii...iiien" with exactly N "i"s
# count_digits( s ):    returns the number of digits in the input string s
# clean_digits( s ):    returns only the digits in the input string s
# clean_word( s ):    returns an all-lowercase, all-letter version of the input string s

