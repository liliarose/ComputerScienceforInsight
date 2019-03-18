# your own data modeling... 
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
#  Let us know which data you're using 
#    + and which columns you're considering features/labels!
#  https://www.kaggle.com/sheenabatra/facebook-data/version/1 --> trying to predict real or fake account 
#  
# writeup: https://docs.google.com/document/d/13l2nGiujZ4aaInO1tcy7ak-ZtngfOiES8WaZRIGvfq8/edit?usp=sharing
#
# This is taken from the titanic example...
#
# Be sure to adapt to your own data!
#
print("+++ Start of pandas' datahandling +++\n")
# df here is a "dataframe":
df = pd.read_csv('facebookac.csv', header=0)    # read the file w/header row #0
#
# drop columns here
#
# df = df.drop('userid', axis=1)  # axis = 1 means column

df.head()                                 # first five lines
df.info()                                 # column details

"""
"""

# One important one is the conversion from string to numeric datatypes!
# You need to define a function, to help out...
def tr_mf(s):
    """ from string to number
    """
    d = { 'male':0, 'female':1 }
    return d[s]

#
# end of conversion to numeric data...
# drop rows with missing data!
df = df.dropna()
#
df['gender'] = df['gender'].map(tr_mf)  # apply the function to the column
"""
Status                          888 non-null object
No Friend                       888 non-null int64
education                       888 non-null object
about me                        888 non-null object
family                          888 non-null object
gender                          888 non-null object
relationship                    888 non-null object
phototag*                       888 non-null int64
photopost*                      888 non-null int64
video                           888 non-null int64
checkin                         888 non-null int64
sport                           888 non-null float64
player                          888 non-null int64
music                           888 non-null int64
film                            888 non-null int64
series                          888 non-null int64
book                            888 non-null int64
game                            888 non-null int64
restaurant                      888 non-null int64
like                            888 non-null int64
group                           888 non-null int64
note                            888 non-null object
post shared/post posted rate    888 non-null float64
"""
def tr_edu(s):
    d = {'university': 0, 'high school': 1, 'no': 2, 'secondary school': 3}
    return d[s]

df['education'] = df['education'].map(tr_edu)

def tr_yn(s):
    d = {"yes":1, "no": 0}
    return d[s]
df['about me'] = df['about me'].map(tr_yn)
df['family'] = df['family'].map(tr_yn)
df['note'] = df['note'].map(tr_yn)
def tr_relation(s):
    d = {'complicate': 78, 'alone': 770, 'married': 15, ' ': 25}
    return d[s]
def tr_status(s):
    d = {'real':1, 'fake': 0}
    return d[s]
df['relationship'] = df['relationship'].map(tr_relation)
df['Status'] = df['Status'].map(tr_status)
print("\n+++ End of pandas +++\n")
df.head()                                 # first five lines
df.info()

#
#
#

print("+++ Start of numpy/scikit-learn +++\n")
# Data needs to be in numpy arrays - these next two lines convert to numpy arrays 
X_all = df.drop('Status', axis=1).values       
y_all = df['Status'].values      
indices = np.random.permutation(len(X_all))
X_data_full = X_all[indices]
y_data_full = y_all[indices]

# randomly choose # to be unlabeled & labeled  
un = 25
X_unlabeled = X_data_full[:un, :]
y_unlabeled = y_data_full[:un]
answers = y_unlabeled

X_labeled = X_data_full[un:, :]
y_labeled = y_data_full[un:]

X_train = X_labeled
y_train = y_labeled


# DT
"""
mdepthv = 0
mdepth = 0
for max_depth in range(210, 230):
    # create our classifier
    dtree = tree.DecisionTreeClassifier(max_depth=max_depth)
    # cross-validate to tune our model (this week, all-at-once)
    scores = cross_val_score(dtree, X_train, y_train, cv=7)
    average_cv_score = scores.mean()
    if average_cv_score > mdepthv:
        mdepthv = average_cv_score
        mdepth = max_depth
    print("      Scores:", scores)
    print("For depth=", max_depth, "average CV score = ", average_cv_score)
print(mdepthv, mdepth)
"""
MAX_DEPTH = 212
# the DT classifier
dtree = tree.DecisionTreeClassifier(max_depth=MAX_DEPTH)
# train it (build the tree)
dtree = dtree.fit(X_train, y_train)
# write out the dtree to tree.dot (or another filename of your choosing...)
filename = 'tree' + str(MAX_DEPTH) + '.dot'
tree.export_graphviz(dtree, out_file=filename,   # the filename constructed above...!
                        filled=True,
                        rotate=False, # True for Left-to-Right; False for Up-Down
                        leaves_parallel=True )  # lots of options!
# Visualize the resulting graphs (the trees) at www.webgraphviz.com
print("Wrote the file", filename)
print("\nChoosing MAX_DEPTH =", MAX_DEPTH, "\n")
# now, train the model with ALL of the training data...  and predict the unknown labels
# our decision-tree classifier...
dtree = tree.DecisionTreeClassifier(max_depth=MAX_DEPTH)
dtree = dtree.fit(X_train, y_train)
# and... Predict the unknown data labels
print("Decision-tree predictions:\n")
predicted_labels = dtree.predict(X_unlabeled)
answer_labels = answers
s = "{0:<11} | {1:<11}".format("Predicted","Answer")
#  arg0: left-aligned, 11 spaces, string, arg1: ditto
print(s)
s = "{0:<11} | {1:<11}".format("-------","-------")
print(s)
# the table...
count = 0
for p, a in zip( predicted_labels, answer_labels ):
    s = "{0:<11} | {1:<11}".format(p,a)
    if not p == a:
        count += 1
    print(s)
print(count)
print("dtree.feature_importances_ are\n      ", dtree.feature_importances_)


print("\n\n")
print("     +++++ Random Forests +++++\n\n")

"""
maxMN = (0, 0, 0)
for m in range(5, 51, 5):
    for n in range(10, 101, 10):
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
MAX_DEPTH = 15 
NUM_TREES = 30
print()
print("Using MAX_DEPTH=", MAX_DEPTH, "and NUM_TREES=", NUM_TREES)
rforest = ensemble.RandomForestClassifier(max_depth=MAX_DEPTH, n_estimators=NUM_TREES)
rforest = rforest.fit(X_train, y_train)

# here are some examples, printed out:
print("Random-forest predictions:\n")
predicted_labels = rforest.predict(X_unlabeled)
answer_labels = answers

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

target_names = ['university', 'high school', 'no', 'secondary school']
print("+++ Start of numpy/scikit-learn +++\n")
# Data needs to be in numpy arrays - these next two lines convert to numpy arrays 
X_all = df.drop('education', axis=1).values       
y_all = df['education'].values      
indices = np.random.permutation(len(X_all))
X_data_full = X_all[indices]
y_data_full = y_all[indices]

# randomly choose # to be unlabeled & labeled  
un = 25
X_unlabeled = X_data_full[:un, :]
y_unlabeled = y_data_full[:un]
answers = y_unlabeled

X_labeled = X_data_full[un:, :]
y_labeled = y_data_full[un:]

X_train = X_labeled
y_train = y_labeled


# DT
"""
mdepthv = 0
mdepth = 0
for max_depth in range(50, 301, 50):
    # create our classifier
    dtree = tree.DecisionTreeClassifier(max_depth=max_depth)
    # cross-validate to tune our model (this week, all-at-once)
    scores = cross_val_score(dtree, X_train, y_train, cv=7)
    average_cv_score = scores.mean()
    if average_cv_score > mdepthv:
        mdepthv = average_cv_score
        mdepth = max_depth
    print("      Scores:", scores)
    print("For depth=", max_depth, "average CV score = ", average_cv_score)
print(mdepthv, mdepth)
"""
MAX_DEPTH = 250
# the DT classifier
dtree = tree.DecisionTreeClassifier(max_depth=MAX_DEPTH)
# train it (build the tree)
dtree = dtree.fit(X_train, y_train)
# write out the dtree to tree.dot (or another filename of your choosing...)
filename = 'tree' + str(MAX_DEPTH) + '.dot'
tree.export_graphviz(dtree, out_file=filename,   # the filename constructed above...!
                        filled=True,
                        rotate=False, # True for Left-to-Right; False for Up-Down
                        leaves_parallel=True )  # lots of options!
# Visualize the resulting graphs (the trees) at www.webgraphviz.com
print("Wrote the file", filename)
print("\nChoosing MAX_DEPTH =", MAX_DEPTH, "\n")
# now, train the model with ALL of the training data...  and predict the unknown labels
# our decision-tree classifier...
dtree = tree.DecisionTreeClassifier(max_depth=MAX_DEPTH)
dtree = dtree.fit(X_train, y_train)
# and... Predict the unknown data labels
print("Decision-tree predictions:\n")
predicted_labels = dtree.predict(X_unlabeled)
answer_labels = answers
s = "{0:<20} | {1:<20}".format("Predicted","Answer")
#  arg0: left-aligned, 11 spaces, string, arg1: ditto
print(s)
s = "{0:<20} | {1:<20}".format("-------","-------")
print(s)
# the table...
count = 0
for p, a in zip( predicted_labels, answer_labels ):
    s = "{0:<20} | {1:<20}".format(target_names[p],target_names[a])
    if not p == a:
        count += 1
    print(s)
print(count)
print("dtree.feature_importances_ are\n      ", dtree.feature_importances_)

"""
print("\n\n")
print("     +++++ Random Forests +++++\n\n")
maxMN = (0, 0, 0)
for m in range(5, 51, 5):
    for n in range(50, 301, 50):
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
MAX_DEPTH = 45 
NUM_TREES = 50
print()
print("Using MAX_DEPTH=", MAX_DEPTH, "and NUM_TREES=", NUM_TREES)
rforest = ensemble.RandomForestClassifier(max_depth=MAX_DEPTH, n_estimators=NUM_TREES)
rforest = rforest.fit(X_train, y_train)

# here are some examples, printed out:
print("Random-forest predictions:\n")
predicted_labels = rforest.predict(X_unlabeled)
answer_labels = answers

s = "{0:<20} | {1:<20}".format("Predicted","Answer")
#  arg0: left-aligned, 11 spaces, string, arg1: ditto
print(s)
s = "{0:<20} | {1:<20}".format("-------","-------")
print(s)
# the table...
count = 0
for p, a in zip( predicted_labels, answer_labels ):
    s = "{0:<20} | {1:<20}".format(target_names[p],target_names[a])
    if not p == a:
        count += 1
    print(s)
# feature importances
print(count)
print("\nrforest.feature_importances_ are\n      ", rforest.feature_importances_)

