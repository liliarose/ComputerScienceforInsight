# titanic5: modeling the Titanic data with DTs and RFs
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
# The "answers" to the 30 unlabeled passengers:
answers = [0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,1,
            1,0,1,1,1,1,0,0,0,1,1,0,1,0]
print("+++ Start of pandas' datahandling +++\n")
# df here is a "dataframe":
df = pd.read_csv('titanic4.csv', header=0)    # read the file w/header row #0
# drop columns here
df = df.drop('name', axis=1)  # axis = 1 means column
# One important one is the conversion from string to numeric datatypes!
# You need to define a function, to help out...
def tr_mf(s):
    """ from string to number
    """
    d = { 'male':0, 'female':1 }
    return d[s]
df['sex'] = df['sex'].map(tr_mf)  # apply the function to the column

# drop rows with missing data!
df = df.drop('body', axis=1)
df = df.drop('cabin', axis=1) # implied in fare
df = df.drop('home.dest', axis=1) # home dest not enough info
df = df.drop('ticket', axis=1) #730 different types of tickets... --> not many in a group 

boats = df["boat"].copy(deep=True)

for i in range(len(boats)):
    if type(boats[i]) == float and np.isnan(boats[i]):
        boats[i] = '-1'

df["boat"] = boats
df = df.dropna()
df.head() 
df.info()
def tr_boat(s):
    d = {'S': 1, 'C': 2, 'Q': 3, '16': 4, '6': 5, '11': 6, '13': 7, '12': 8, '10': 9, '5': 10, '4': 11, '8': 12, '2': 13, '3': 14, 'D': 15, '9': 16, 'B': 17, 'A': 18, '7': 19, '14': 20, '5 9': 21, '1': 22, '15': 23, '5 7': 24, '8 10': 25, '13 15 B': 26, 'C D': 27, '13 15': 28, '-1':29}
    return d[s]
df['boat'] = df['boat'].map(tr_boat)

def embarkTr(s):
    """ from string to number
    """
    d = {'S': 0, 'C':1, 'Q':2}
    return d[s]
df['embarked'] = df['embarked'].map(embarkTr)

# end of conversion to numeric data...
print("\n+++ End of pandas +++\n")
print("+++ Start of numpy/scikit-learn +++\n")
# Data needs to be in numpy arrays - these next two lines convert to numpy arrays 
X_all = df.drop('survived', axis=1).values       
y_all = df[ 'survived' ].values      
un = 30
X_unlabeled = X_all[:un, :]
y_unlabeled = y_all[:un]

X_labeled_orig = X_all[un:, :]
y_labeled_orig = y_all[un:]
indices = np.random.permutation(len(X_labeled_orig))
X_labeled = X_labeled_orig[indices]              # we apply the same permutation to each!
y_labeled = y_labeled_orig[indices]

X_train = X_labeled 
y_train = y_labeled 
print(X_train)
print(y_train)
#
# now, building from iris5.py and/or digits5.py
#      create DT and RF models on the Titanic dataset!
#
#      Goal: find feature importances ("explanations")
#      Challenge: can you get over 80% CV accuracy?
#
"""
# best one: 
# Scores: [0.96078431 0.96078431 0.96534653 0.95544554 0.9800995 ]
# For depth= 1 average CV score =  0.9644920418292926
# 0.9644920418292926 1


feature_names = ["pclass", "sex", "age", "sibsp", "parch", "fare", "embarked", "boat"]
target_names = ["0", "1"]
mdepthv = 0
mdepth = 0
for max_depth in range(1, 2):
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
for max_depth in range(1, 2): #[1,2,3]:
    # the DT classifier
    dtree = tree.DecisionTreeClassifier(max_depth=max_depth)
    # train it (build the tree)
    dtree = dtree.fit(X_train, y_train)
    # write out the dtree to tree.dot (or another filename of your choosing...)
    filename = 'tree' + str(max_depth) + '.dot'
    tree.export_graphviz(dtree, out_file=filename,   # the filename constructed above...!
                            filled=True,
                            rotate=False, # True for Left-to-Right; False for Up-Down
                            leaves_parallel=True )  # lots of options!
    # Visualize the resulting graphs (the trees) at www.webgraphviz.com
    print("Wrote the file", filename)
MAX_DEPTH = 1   # choose a MAX_DEPTH based on cross-validation... 
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
    if not p == a:
        print("n", s)
    print(s)
#
# feature importances!
#
print()
print("dtree.feature_importances_ are\n      ", dtree.feature_importances_)


print("\n\n")
print("     +++++ Random Forests +++++\n\n")
"""
maxMN = (0, 0, 0)
for m in range(1,10):
    for n in range(1, 202, 25):
        rforest = ensemble.RandomForestClassifier(max_depth=m, n_estimators=n)
        # an example call to run 5x cross-validation on the labeled data
        scores = cross_val_score(rforest, X_train, y_train, cv=5)
        if scores.mean() > maxMN[-1]:
            maxMN = (m, n, scores.mean())
            print("for max_depth", m, "and n_estimators", n, "CV scores:", scores)
            print("CV scores' average:", scores.mean())
    print(maxMN)
    # input(">")
"""
MAX_DEPTH = 3 
NUM_TREES = 35 
print()
print("Using MAX_DEPTH=", MAX_DEPTH, "and NUM_TREES=", NUM_TREES)
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
count = 0
for p, a in zip( predicted_labels, answer_labels ):
    s = "{0:<11} | {1:<11}".format(p,a)
    if not a == p:
        count +=1
    print(s)
# feature importances
print(count)
print("\nrforest.feature_importances_ are\n      ", rforest.feature_importances_)
input(">")

# the best one: 
# for max_depth 3 and n_estimators 35 CV scores: [0.97058824 0.96568627 0.97029703 0.97029703 0.95024876]
# CV scores' average: 0.9654234650857536        (3, 35, 0.9654234650857536)
"""
rforest.feature_importances_ are
       [0.07258494 0.15678027 0.03316166 0.01767886 0.00745414 0.06592394
 0.00934192 0.63707426]

Predicted   | Answer
-------     | -------
0           | 0
0           | 0
0           | 0
0           | 0
1           | 0
0           | 0
0           | 1
1           | 0
1           | 0
1           | 0
1           | 0
1           | 0
1           | 1
1           | 0
0           | 1
0           | 1
0           | 1
0           | 0
1           | 1
1           | 1
1           | 1
1           | 1
0           | 0
1           | 0
1           | 0
1           | 1
0           | 1
0           | 0
1           | 1
0           | 0
"""
