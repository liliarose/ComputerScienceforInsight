# titanic.py
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
df = pd.read_csv('titanic4.csv', header=0)
df.head()
df.info()
df = df.drop('body', axis=1)  # axis = 1 indicates we want to drop a column, not a row
df = df.drop('cabin', axis=1) # implied in fare
df = df.drop('boat', axis=1) # not enough info
df = df.drop('home.dest', axis=1) # home dest not enough info
df = df.drop('name', axis=1) # doesn't seem it will affect the result?
df = df.drop('ticket', axis=1) #730 different types of tickets... --> not many in a group 
df = df.dropna()
# careful!  You will need to drop more columns before dropping all of the N/A data!

# let's see our dataframe again...
# after some data-wrangling, I ended up with 1001 rows (anything over 500-600 seems reasonable)
df.head()
df.info()
"""
pclass      1043 non-null int64
survived    1043 non-null int64
sex         1043 non-null object
age         1043 non-null float64
sibsp       1043 non-null int64
parch       1043 non-null int64
fare        1043 non-null float64
embarked    1043 non-null object
"""

# You'll need conversion to numeric datatypes for all input columns
#   Here's one example

def genderTr(s):
    """ from string to number
    """
    d = { 'male':2, 'female':3 }
    return d[s]

df['sex'] = df['sex'].map(genderTr)  # apply the function to the column
# defaultdict(int, {'S': 781, 'C': 212, 'Q': 50})

def embarkTr(s):
    """ from string to number
    """
    d = {'S': 0, 'C':1, 'Q':2}
    return d[s]

df['embarked'] = df['embarked'].map(embarkTr)
# let's see our dataframe again...

df.head()
df.info()
# you may need others!

print("+++ end of pandas +++\n")

# import sys
# sys.exit(0)

# separate into input X and target y dataframes...
X_all_df = df.drop('survived', axis=1)        # everything except the 'survival' column

y_all_df = df[ 'survived' ]                   # the target is survival! 
X_all = X_all_df.values 
y_all = y_all_df.values

un = 42 # unlabeled # 
X_unlabeled = X_all[:un, :]
y_unlabeled = y_all[:un]

X_labeled_orig = X_all[un:, :]  
y_labeled_orig = y_all[un:]    
indices = np.random.permutation(len(X_labeled_orig))
X_labeled = X_labeled_orig[indices]              # we apply the same permutation to each!
y_labeled = y_labeled_orig[indices]

print("+++ start of numpy/scikit-learn +++")
# Use iris4.py as your guide - it's mostly copy-and-paste
# BUT -- there are points where things diverge...
# AND -- the goal is that you understand and feel more and more comfortable
#        with each of the parts of "the machine learning pipeline" ... !
# Note: for the Titanic data, it's the first 42 passengers who are unlabeled
"""
TEST_SIZE = 100 
X_test = X_labeled[:TEST_SIZE]    # first few are for testing
y_test = y_labeled[:TEST_SIZE]

X_train = X_labeled[TEST_SIZE:]   # all the rest are for training
y_train = y_labeled[TEST_SIZE:]
"""
testStart = 0
testEnd= 42
X_all= X_all[:,:]  # unlabeled up to index 9
y_all= y_all[:]    # unlabeled up to index 9

X_test = X_all[testStart:testEnd]
y_test = y_all[testStart:testEnd]
X_train = X_all[testEnd:]
y_train = y_all[testEnd:]

from sklearn.neighbors import KNeighborsClassifier


def cross_validation_test(k, X_train, y_train):
    knn = KNeighborsClassifier(n_neighbors=k)
    cv_scores = cross_val_score( knn, X_train, y_train, cv=5 )
    av = cv_scores.mean()
    if av >= .7:
        print('\nthe cv_scores are')
        for s in cv_scores:
            # we format it nicely...
            s_string = "{0:>#7.4f}".format(s) # docs.python.org/3/library/string.html#formatexamples
            print("   ",s_string)
        av = cv_scores.mean()
    print('+++ with average: ', av, '\n')
    return av
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


def lrescale(arr, value, col=2):
    """
        linear rescale?
        age ind == 2?
    """
    arr2 = arr.astype(float)
    for elem in arr2:
        arr2[col] =  elem/value
    return arr2

def powRescale(arr, value, col=2):
    arr2 = arr.astype(float)
    for elem in arr2:
        arr2[col] =  elem**value
    return arr2

X_trainT = powRescale(X_train, 1/2, 6)
X_testT = powRescale(X_test, 1/2, 6)
# for k in range(15, 31, 2):
t = cross_validation_test(23, X_trainT, y_train)
actualTesting(X_train, y_train, X_test, y_test, best_k=25)
"""
Comments and results:

Briefly mention how this went:
  + what value of k did you decide on for your kNN?
  + how high were you able to get the average cross-validation (testing) score?
    for k, I tried many times with cv test, but always got sth b/w 15 to 29, and decided to settle 23 (somewhere in the middleish)
    the highest I ever got was .698... 
Then, include the predicted survival of the unlabeled data (in the original order).
    [0 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 1 1 1 1 0 1 1 1 1 1 1 1 1 1 0 1 0 0 0 0 0 1 0 1]
We'll share the known results next week... :-)

"""
