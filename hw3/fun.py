#
# fun.py
# 
# fun example of Python import fun!
#

def fac(x):
    """ factorial function """
    if x < 2: 
        return 1
    return x*fac(x-1)

if __name__ == "__main__":
    print("Hi there ~ from fun.py!")





#
# numpy examples...
#

# np.arange(0,1,.25)
# np.linspace(0,1,5)
# np.ones( (4,2) )   # shape=(4,2)
# np.zeros( 3 )

# from numpy.random import rand
# A = rand(2,4)
# L = np.ndarray.tolist(A)
# A = np.asarray(L)

"""
A[1:3][
L = [ range(low,low+6) for low in range(0,60,10) ]
A = np.asarray( L )
A[1:3,0:2]

" Quiz! "
A[1:3,0:2]
A[0,3:5]
A[4:,4:]
A[:,2]
A[2::2,::2]
" end of quiz "

Tricky!!    What's this:  A[1:3][0:2]  and why!?
"""

# 42 * [4,2]
# 42 * np.array( [4,2] )