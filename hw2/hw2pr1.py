#
# hw2pr1.py - write-your-own-web-engine...
# then, improve the page's content and styling!
import re
from copy import deepcopy
import os 
import webbrowser 

def apply_headers( OriginalLines ):
    """ should apply headers, h1-h5, as tags
        # * i --> <h[i]>
        returns new list of lines 
    """
    # loop for all headings: h1-h5
    NewLines =[]
    for line in OriginalLines:
        for i in range(5):
            x = 5-i
            if line.startswith('#'*x):
                # print("original:", line)
                line = "<h" + str(x) + ">" + line[x:] + "</h" + str(x) + ">"
                # print("new:", line)
                break
        NewLines += [ line ]
    return NewLines

def addBlinkCss(filename):
    blink = "blink{-moz-animation-duration: 4ms; -moz-animation-name: blink; -moz-animation-iteration-count: infinite; -moz-animation-direction: alternate; -webkit-animation-duration: 400ms; -webkit-animation-name: blink; -webkit-animation-iteration-count: infinite; -webkit-animation-direction: alternate; animation-duration: 400ms; animation-name: blink; animation-iteration-count: infinite; animation-direction: alternate;}@-moz-keyframes blink{from{opacity: 1;}to{opacity: 0;}}@-webkit-keyframes blink{from{opacity: 1;}to{opacity: 0;}}@keyframes blink{from{opacity: 1;}to{opacity: 0;}}"
    with open(filename, "a") as myfile:
        myfile.write(blink)

def apply_wordstyling( OriginalLines ):
    """
        changes the following for what they want 
        --blink --
        ~~strikethrough~~
        ~italic~
        *bold*
        @link@
        _underscore_
        ___ (horizontal rule)
    """
    # loop for the word-stylings: here, ~word~
    NewLines =[]
    # add blink css to css file --> assumes it to be "starter.css" 
    addBlinkCss("starter.css")

    for line in OriginalLines:
        # ___ (horizontal rule)
        line = re.sub(r"___", r"<hr>", line)
        # --blink -- 
        line = re.sub(r"--(.*)--", r"<blink>\1</blink>", line)
        # ~~strikethrough~~
        line = re.sub(r"~~(.*)~~", r"<strike>\1</strike>", line)
        # italic 
        line = re.sub(r"~(.*)~", r"<i>\1</i>", line)
        # *bold*
        line = re.sub(r"\*(.*)\*", r"<b>\1</b>", line)
        # @link@
        line = re.sub(r"@(.*)@", r'<a href="\1"> \1 </a>', line)
        # _underscore_
        line = re.sub(r"_(.*)_", r"<u>\1</u>", line)
        NewLines += [line]
    return NewLines
    # Your task: add at least
    #   *bold*
    #   @link@  (extra: use a regular expression to match a link!)
    #   _underscore_
    #   extra-credit!  BLINKING (working!) or strikethrough
    #   remember for many special symbols, you need to "backslash" them...

def listify(OriginalLines):
    """ convert lists beginning with "   +" into HTML """
    NewLines = []
    # loop for lists
    first = True # if first and is list --> add list 
    for line in OriginalLines:
        if line.startswith("   +"):
            if first:
                line = "<ul>\n<li>" + line[4:] + "</li>\n"
                first = False 
            else:
                line = "<li>" + line[4:] + "</li>\n"
        elif not first:
            line = "</ul>\n" + line
            first = True 
        NewLines += [line]
        # note - this is wrong: your challenge: fix it!
    return NewLines



def main():
    """ handles the conversion from the human-typed file to the HTML output """

    HUMAN_FILENAME = "starter.txt"
    OUTPUT_FILENAME = "starter.html"

    f = open(HUMAN_FILENAME, "r", encoding="latin1")
    contents = f.read()
    f.close()
    # webbrowser.open("file://"+os.getcwd()+"/"+HUMAN_FILENAME)
    OriginalLines = contents.split("\n")  # split to create a list of lines 
    NewLines = apply_headers( OriginalLines )
    NewLines = apply_wordstyling(NewLines)
    NewLines = listify(NewLines)

    # finally, we join everything with newlines...
    final_html = '\n'.join(NewLines)

    # print("\nFinal contents are\n", final_html, "\n")

    f = open(OUTPUT_FILENAME, "w")     # write this out to a file...
    f.write( final_html )
    f.close()
    webbrowser.open("file://"+os.getcwd()+"/"+OUTPUT_FILENAME)
    # then, render in your browser...


if __name__ == "__main__":
    main()


