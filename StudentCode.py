import pandas as pd
import numpy as np
import sklearn
from sklearn import metrics
from sklearn import preprocessing
    
from sklearn.naive_bayes import GaussianNB

#New Libraries:
#from sklearn.tree import DecisionTreeClassifier
#from sklearn.tree import export_graphviz

import sys
if sys.version_info >= (3, 0):
    print("Error: You are running Python 3.x. This pynb is written in Python 2.")


# Load data
bc = pd.read_csv('breast-cancer.csv', header=None)

header_labels = []
with open("field_names.txt") as header_labels_file:
    print "Column Headers:\n"
    for line in header_labels_file:
        header_labels.append(line.strip())
for label in header_labels:
    print label
print "\nNumber of labels loaded: %.f" %len(header_labels)

bc.columns=header_labels

#Preprocessing, and Randomization
bc=bc.sample(frac=1,random_state=5).reset_index(drop=True)
bc_Y = pd.get_dummies(bc.diagnosis)
bc_Y = bc_Y.drop('B',1)
bc_Y.columns = ['diagnosis_M',]

bc_X = bc.drop('diagnosis', 1).drop('ID', 1)

bc_cols = bc_X.columns
X = bc_X.values #returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
X_scaled = min_max_scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled)
X_scaled.columns = bc_cols


#Splitting Test/Train Data
train_data,train_labels = X_scaled[:450],bc_Y[:450]
test_data,test_labels = X_scaled[450:],bc_Y[450:]
print "Test data, Malignant ratio [%.2f]:\t%.0f out of %.0f" % (float(
        test_labels[test_labels.diagnosis_M==1].shape[0]/1./test_labels.shape[0]),
                                                                test_labels[test_labels.diagnosis_M==1].shape[0],
                                                                test_labels.shape[0])
print "Training data, Malignant ratio [%.2f]:\t%.0f out of %.0f" % (float(
        train_labels[train_labels.diagnosis_M==1].shape[0]/1./train_labels.shape[0]),
                                                                    train_labels[train_labels.diagnosis_M==1].shape[0],
                                                                    train_labels.shape[0])

#Create an ML Model
bc_NewModel = GaussianNB()

bc_NewModel.fit(train_data.values,train_labels.values.ravel())
model_predictions = bc_NewModel.predict(test_data.values)

#Print Results Summary
print "\n"
print bc_NewModel
print "SKLearn calc accuracy:\t\t\t%.2f%%" % float(100*sklearn.metrics.accuracy_score(model_predictions,test_labels))
print "SKLearn calc accuracy (true diag B):\t%.2f%%" % float(100*sklearn.metrics.accuracy_score(model_predictions[test_labels.diagnosis_M.values==0],test_labels[test_labels.diagnosis_M.values==0]))
print "SKLearn calc accuracy (true diag M):\t%.2f%%" % float(100*sklearn.metrics.accuracy_score(model_predictions[test_labels.diagnosis_M.values==1],test_labels[test_labels.diagnosis_M.values==1]))
print "SKLearn calc f1 score:\t%.2f" % sklearn.metrics.f1_score(model_predictions,test_labels)
print "\n"

