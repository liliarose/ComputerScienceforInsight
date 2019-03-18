#
# three.py
#

from PIL import Image

im = Image.open( "digit1.png" )

print("im is of size", im.size)

im_resized = im.resize( (8,8), Image.BICUBIC )

ir = im_resized

for row in range(8):
    for col in range(8):
        r, g, b, a = ir.getpixel( (col,row) )
        pixstring = "{0:3d}, ".format(r)  # cool Python formatting!
        print( pixstring, end="")
    print()


