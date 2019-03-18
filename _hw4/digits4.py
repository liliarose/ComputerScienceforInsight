#
#
# digits4.py
#
#

import numpy as np
from sklearn import datasets
import pandas as pd


try: # different imports for different versions of scikit-learn
    from sklearn.model_selection import cross_val_score   # simpler cv this week
except ImportError:
    try:
        from sklearn.cross_validation import cross_val_score
    except:
        print("No cross_val_score!")



# For Pandas's read_csv, use header=0 when you know row 0 is a header row
# df here is a "dataframe":
df = pd.read_csv('digits4.csv', header=0)
df.head()
df.info()

# Convert feature columns as needed...
# You may to define a function, to help out:
def transform(s):
    """ from number to string
    """
    return 'digit ' + str(s)
    
df['label'] = df['64'].map(transform)  # the label in column 64
print("+++ End of pandas +++\n")

# import sys
# sys.exit(0)

# separate the data into input X and target y dataframes...
X_all_df = df.drop('label', axis=1)        # everything except the 'label' column
y_all_df = df[ 'label' ]                   # the label is the target! 

print("+++ start of numpy/scikit-learn +++")

# The data is currently in pandas "dataframes," but needs to be in numpy arrays
# These next two lines convert two dataframes to numpy arrays (using .values)
X_all = X_all_df.values        # iloc == "integer locations" of rows/cols
y_all = y_all_df.values      # individually addressable columns (by name)


#
# Use iris4.py as your guide - it's "mostly" copy-and-paste
# HOWEVER -- there are points where things diverge...
# AND -- our goal is that you understand and feel more and more comfortable
#        with each of the parts of "the machine learning pipeline" ... !
#


#
# Also: for the digits data...
#     + the first 10 rows [0:10] are unlabeled AND have only partial data!
#     + the next 12 rows [10:22] are unlabeled but have full data... .
#
# You should create TWO sets of unlabeled data to be predicted.
#     + extra credit:  predict the missing pixels themselves!
#













"""
Comments and results:

Briefly mention how this went:
  + what value of k did you decide on for your kNN?
  + how smoothly were you able to adapt from the iris dataset to here?
  + how high were you able to get the average cross-validation (testing) score?



Then, include the predicted labels of the 12 full-data digits with no label
Past those labels (just labels) here:

You'll have 12 digit labels:




And, include the predicted labels of the 10 digits that are "partially erased" and have no label:
Mention briefly how you handled this situation!?

Only use the top half to train your code. Do not train it using the bottom half.
This one had a lower testing-data score but both of them often had a 1.0 training-data score.

Past those labels (just labels) here:
You'll have 10 lines:






If you predicted the pixels themselves, cool! Share those, as well. (This is Ex. Cr.)


"""









#
# feature display - use %matplotlib to make this work smoothly
#


def show_digit( Pixels ):
    """ input Pixels should be an np.array of 64 integers (valued between 0 to 15) 
        there's no return value, but this should show an image of that 
        digit in an 8x8 pixel square
    """
    from matplotlib import pyplot as plt
    print(Pixels.shape)
    Patch = Pixels.reshape((8,8))
    plt.figure(1, figsize=(4,4))
    plt.imshow(Patch, cmap=plt.cm.gray_r, interpolation='nearest')  # plt.cm.gray_r   # plt.cm.hot
    plt.show()
    
# try it!
if False:
    row = 9 + 22
    Pixels = X_all[row:row+1,:]
    #show_digit(Pixels)
    print("That image has the label:", y_all[row])

# another try
if False:
    row = 5 + 22
    Pixels = X_all[row:row+1,:]
    #show_digit(Pixels)
    print("That image has the label:", y_all[row])


