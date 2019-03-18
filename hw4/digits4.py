# digits4.py
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
    return str(s)
    
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

# all unlabeled 
X_unlabeled = X_all[:22,:]
y_unlabeled = y_all[:22]
# the ones missing 
y_unlabeledM = y_unlabeled[:10]
y_unlabeled = y_unlabeled[10:]
X_unlabeledM = X_unlabeled[:10]
X_unlabeled = X_unlabeled[10:]

# the labeled ones 

X_labeledO = X_all[22:,:]
y_labeledO = y_all[22:]

indices = np.random.permutation(len(y_labeledO))

X_labeled = X_labeledO[indices] 
y_labeled = y_labeledO[indices]
print("INDICES", indices)

from sklearn.neighbors import KNeighborsClassifier


# Use iris4.py as your guide - it's "mostly" copy-and-paste
# HOWEVER -- there are points where things diverge...
# AND -- our goal is that you understand and feel more and more comfortable
#        with each of the parts of "the machine learning pipeline" ... !

def cross_validation_test(k, X_train, y_train, wtype='uniform'):
    knn = KNeighborsClassifier(n_neighbors=k, weights=wtype)
    cv_scores = cross_val_score( knn, X_train, y_train, cv=5 )
    av = cv_scores.mean()
    if av >= .9886:
        print('\nthe cv_scores are')
        for s in cv_scores:
            # we format it nicely...
            s_string = "{0:>#7.4f}".format(s) # docs.python.org/3/library/string.html#formatexamples
            print("   ",s_string)
        av = cv_scores.mean()
    print('+++ with average: ', av, '\n') 

"""
for k in range(1, 153, 2):
    print("for value k =", k)
    for test in range(3):
        cross_validation_test(k, X_train, y_train)
    userCue = input('>')
best k @ k = 3
"""
def actualTesting(X_train, y_train, X_test, y_test, best_k = 3, wtype="uniform"):
    knn_train = KNeighborsClassifier(n_neighbors=best_k, weights='uniform')
    knn_train.fit(X_train, y_train)
    print("\nCreated and trained a knn classifier with k =", best_k)
    print("For the input data in X_test,")
    predicted_labels = knn_train.predict(X_test)
    actual_labels = y_test
    print("The predicted outputs are\n", predicted_labels)
    print("and the actual labels are\n", actual_labels, '\n')
    s = "{0:<11} | {1:<11}".format("Predicted","Actual")
    print(s)
    s = "{0:<11} | {1:<11}".format("-------","-------")
    print(s)
    for pi, ai in zip( predicted_labels, actual_labels):
        # if not pi == ai:
            # print("check next")
        s = "{0:<11} {1:<11}".format(pi, ai)
        print(s)
    print("\n\n")

def reweight(arr, value, c):
    arr2 = arr.astype(float)
    arr2[c] *= value
    return arr2 
# Also: for the digits data...
#     + the first 10 rows [0:10] are unlabeled AND have only partial data!
#     + the next 12 rows [10:22] are unlabeled but have full data... .
#
# You should create TWO sets of unlabeled data to be predicted.
#     + extra credit:  predict the missing pixels themselves!
#
X_test = X_labeled[:10]
X_train = X_labeled[10:]
y_test = y_labeled[:10]
y_train = y_labeled[10:]

# actualTesting(X_train, y_train, X_test, y_test)

X_test = X_unlabeled
y_test = y_unlabeled 
X_train = X_labeled
y_train = y_labeled
X_trainT = reweight(X_train, .7, 0)
X_testT = reweight(X_test, .7, 0)
actualTesting(X_trainT, y_train, X_testT, y_test, best_k=7)

# for first 10 partial-data digits 
# erase last 

"""
for r in [0,1, 6, 7]:
    for c in range(10):
        for k in range(3, 11, 2):
            print("reweight", r, "by", c*.1, 'and k =', k)
            X_trainT = reweight(X_train, c*.1, r)
            X_testT = reweight(X_test, c*.1, r)
            actualTesting(X_trainT, y_train, X_testT, y_test, best_k=k)
            uc = input('>')
"""

X_testT = X_unlabeledM
y_test = y_unlabeledM
X_trainT = X_labeled[:len(X_labeled)//2]
y_train = y_labeled[:len(X_labeled)//2]

# erase last 3 rows (24 digits) or 26 digits possibly?

for i in range(25):
    X_trainT = reweight(X_trainT, 0.0, -i)
    actualTesting(X_trainT, y_train, X_testT, y_test, best_k=7)
    uc = input('>')


"""
Comments and results:

Briefly mention how this went:
  + what value of k did you decide on for your kNN?
  + how smoothly were you able to adapt from the iris dataset to here?
  + how high were you able to get the average cross-validation (testing) score?

Only doing the cv validation, 3 always had the highest average, but w/ the missing labels it wasn't the case


I experimented with for looping & changing the values 0&1, and got that for values 0&1 were most insensitive and that k=5-9 was the best 


Then, include the predicted labels of the 12 full-data digits with no label
Past those labels (just labels) here:

You'll have 12 digit labels:
The predicted outputs are
 ['9' '9' '5' '5' '6' '5' '0' '9' '8' '9' '8' '4']

And, include the predicted labels of the 10 digits that are "partially erased" and have no label:
Mention briefly how you handled this situation!?
The erased row would definitely have not contribution, so I ignored them in the original training data 

Only use the top half to train your code. Do not train it using the bottom half.
This one had a lower testing-data score but both of them often had a 1.0 training-data score.

Past those labels (just labels) here:
You'll have 10 lines:
['0' '0' '0' '1' '7' '7' '3' '4' '0' '1']

If you predicted the pixels themselves, cool! Share those, as well. (This is Ex. Cr.)


"""


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

testing = False 
if testing:
    row = 9 + 22
    Pixels = X_all[row:row+1,:][:64]
    print(len(Pixels))
    show_digit(Pixels)
    print("That image has the label:", y_all[row])

# another try
if testing:
    row = 5 + 22
    Pixels = X_all[row:row+1,:][:64]
    show_digit(Pixels[:64])
    print("That image has the label:", y_all[row])


