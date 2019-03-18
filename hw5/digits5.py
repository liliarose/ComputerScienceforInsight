# digits5: modeling the digits data with DTs and RFs
import numpy as np            
import pandas as pd
from sklearn import tree      # for decision trees
from sklearn import ensemble  # for random forests

try: # different imports for different versions of scikit-learn
    from sklearn.model_selection import cross_val_score   # simpler cv this week
except ImportError:
    try:
        from sklearn.cross_validation import cross_val_score
    except:
        print("No cross_val_score!")

# The "answers" to the 20 unknown digits, labeled -1:
answers = [9,9,5,5,6,5,0,9,8,9,8,4,0,1,2,3,4,5,6,7]

print("+++ Start of pandas' datahandling +++\n")
# df here is a "dataframe":
df = pd.read_csv('digits5.csv', header=0)    # read the file w/header row #0
df.head()                                 # first five lines
df.info()                                 # column details
print("\n+++ End of pandas +++\n")

print("+++ Start of numpy/scikit-learn +++\n")
# Data needs to be in numpy arrays - these next two lines convert to numpy arrays
X_all = df.iloc[:,0:64].values        # iloc == "integer locations" of rows/cols
y_all = df[ '64' ].values      # individually addressable columns (by name)

X_unlabeled = X_all[:20,:]  # the "unknown" flower species (see above!)
y_unlabeled = y_all[:20]    # these are "unknown"

X_labeled = X_all[20:,:]  # make the 10 into 0 to keep all of the data
y_labeled = y_all[20:]    # same for this line

# we can scramble the data - but only the labeled data!
indices = np.random.permutation(len(X_labeled))  # this scrambles the data each time
X_data_full = X_labeled[indices]
y_data_full = y_labeled[indices]

# Notice that, here, we will _only_ use cross-validation for model-buidling
#   (We won't include a separate X_train X_test split.)
X_train = X_data_full
y_train = y_data_full
"""
m =4 
maxMN = (0, 0, 0)
for n in range(240, 261, 5):
    rforest = ensemble.RandomForestClassifier(max_depth=m, n_estimators=n)
    # an example call to run 5x cross-validation on the labeled data
    scores = cross_val_score(rforest, X_train, y_train, cv=5)
    if scores.mean() > maxMN[-1]:
        maxMN = (m, n, scores.mean())
    print("for max_depth", m, "and n_estimators", n, "CV scores:", scores)
    print("CV scores' average:", scores.mean())
print(maxMN)
input(">")
mdepthv = 0
mdepth = 0
for max_depth in range(140, 160):
    # create our classifier
    dtree = tree.DecisionTreeClassifier(max_depth=max_depth)
    # cross-validate to tune our model (this week, all-at-once)
    scores = cross_val_score(dtree, X_train, y_train, cv=5)
    average_cv_score = scores.mean()
    if average_cv_score > mdepthv:
        mdepthv = average_cv_score
        mdepth = max_depth
    print("      Scores:", scores)
    print("For depth=", max_depth, "average CV score = ", average_cv_score)
print(mdepthv, mdepth)
"""

MAX_DEPTH = 150   # choose a MAX_DEPTH based on cross-validation... 
print("\nChoosing MAX_DEPTH =", MAX_DEPTH, "\n")
# now, train the model with ALL of the training data...  and predict the unknown labels
# our decision-tree classifier...
dtree = tree.DecisionTreeClassifier(max_depth=MAX_DEPTH)
dtree = dtree.fit(X_train, y_train)
# and... Predict the unknown data labels
print("Decision-tree predictions:\n")
predicted_labels = dtree.predict(X_unlabeled)
answer_labels = answers

# formatted printing! (docs.python.org/3/library/string.html#formatstrings)
s = "{0:<11} | {1:<11}".format("Predicted","Answer")
#  arg0: left-aligned, 11 spaces, string, arg1: ditto
print(s)
s = "{0:<11} | {1:<11}".format("-------","-------")
print(s)
# the table...
for p, a in zip( predicted_labels, answer_labels ):
    s = "{0:<11} | {1:<11}".format(p,a)
    print(s)

#
# feature importances!
#
print()
print("dtree.feature_importances_ are\n      ", dtree.feature_importances_)

MAX_DEPTH = 4
NUM_TREES = 260
print("\nUsing MAX_DEPTH=", MAX_DEPTH, "and NUM_TREES=", NUM_TREES)
rforest = ensemble.RandomForestClassifier(max_depth=MAX_DEPTH, n_estimators=NUM_TREES)
rforest = rforest.fit(X_train, y_train)

# here are some examples, printed out:
print("Random-forest predictions:\n")
predicted_labels = rforest.predict(X_unlabeled)
answer_labels = answers  # because we know the answers, above!

#
# formatted printing again (see above for reference link)
#
s = "{0:<11} | {1:<11}".format("Predicted","Answer")
#  arg0: left-aligned, 11 spaces, string, arg1: ditto
print(s)
s = "{0:<11} | {1:<11}".format("-------","-------")
print(s)
# the table...
for p, a in zip( predicted_labels, answer_labels ):
    s = "{0:<11} | {1:<11}".format(p,a)
    print(s)
# feature importances
print("\nrforest.feature_importances_ are\n      ", rforest.feature_importances_)
# print("Order:", feature_names[0:20])

#
# now, model from iris5.py to try DTs and RFs on the digits dataset!



"""
    DT was not as good as RF, which about the same as knn?

dtree.feature_importances_ are
       [0.         0.         0.00801527 0.01093525 0.00093296 0.06264365
 0.01508272 0.         0.         0.00321219 0.0187707  0.00207695
 0.01226192 0.02105368 0.00062847 0.         0.00123905 0.00457071
 0.01879474 0.01896108 0.04083999 0.07597264 0.00199016 0.
 0.0012479  0.00326806 0.01433916 0.05068756 0.00643381 0.04403869
 0.00083796 0.         0.         0.10463933 0.02767418 0.01017823
 0.07226867 0.02264765 0.00576271 0.         0.         0.00599261
 0.0778812  0.05407709 0.01483461 0.00447995 0.00313402 0.
 0.         0.         0.00954117 0.00948828 0.00836869 0.01481338
 0.02535257 0.         0.         0.         0.01721306 0.00213681
 0.06134728 0.00249893 0.00620581 0.00062847]

rforest.feature_importances_ are
       [0.00000000e+00 1.22342281e-03 2.01052848e-02 2.41428072e-03
 1.41623142e-03 1.13635947e-02 7.10273883e-03 2.19090338e-04
 0.00000000e+00 8.99785796e-03 3.11900887e-02 1.22619138e-03
 4.37610647e-03 3.14336751e-02 1.66977899e-03 2.10423594e-05
 0.00000000e+00 3.72691763e-03 9.48889699e-03 2.08334835e-02
 3.04474798e-02 6.51077991e-02 4.60389629e-03 3.34813877e-05
 0.00000000e+00 1.07595508e-02 5.00821291e-02 1.89973097e-02
 4.24994066e-02 2.14052362e-02 4.46966907e-02 0.00000000e+00
 0.00000000e+00 4.33806539e-02 2.76737882e-02 1.49680590e-02
 6.12696579e-02 1.27560031e-02 2.65622771e-02 0.00000000e+00
 0.00000000e+00 1.35714906e-02 4.24225313e-02 5.62716426e-02
 1.97369079e-02 1.19270095e-02 2.79030367e-02 0.00000000e+00
 0.00000000e+00 5.53815685e-04 1.06469238e-02 1.04103249e-02
 8.27680176e-03 2.08554221e-02 3.25187511e-02 6.49349064e-04
 0.00000000e+00 9.70346670e-04 1.96122352e-02 2.42925113e-03
 3.20412729e-02 3.80330450e-02 1.70855163e-02 2.03222419e-03] 

"""
