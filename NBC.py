# -*- coding: utf-8 -*-

# create a vector
import numpy as np

# for clean console output, let's suppress them for now.
import warnings
warnings.filterwarnings("ignore")

# get data from csv
import csv

import os
aBasePath = os.getcwd()
globalCSVDataStorePath = aBasePath+"/../TextSentiment.V1.b/twitterData/myJsonOutput.csv"


# get a classifier
from sklearn import cross_validation, metrics
from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB(alpha=0.1, class_prior=None, fit_prior=True)


TagMapperDictionary = {"anger":0,"anticipation":1,"disgust":2,"enjoyment":3,"fear":4,"sad":5,"surprise":6,"trust":7}
TagMapperList = ["anger" , "anticipation" , "disgust" , "enjoyment" , "fear" , "sad" , "surprise" , "trust"]

def RepresentsNum(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def GetTrainVectors(filePath):
    with open(filePath, 'rb') as csvfile:
        readFile = csv.reader(csvfile, delimiter=',')
        X = None
        y = None
        for row in readFile:
            # aRow = row[-1]
            listStrA = row[3]
            listStr1 = row[5]
            listStr2 = listStr1[1:-1]
            listStr3 = listStr2.split()
            listVector = [float(i) for i in listStr3 if RepresentsNum(i)]

            # print (type(row), len(row), listVector)
            # newrow = [1,2,3]
            # print(">>", len(listVector), listVector)

            if len(listVector) != 0:
                assert (len(listVector) == 8) # emo-vector length should be 8;
                if True: # Training Only
                    emoTypesCount = 0
                    for i in range(0,8,1):
                        if (listVector[i] > 0.0):
                            emoTypesCount += 1

                    if (emoTypesCount == 0):
                        emoLabel = 8 # "neutral"     # Future Road Map Label
                        break
                    elif (emoTypesCount <= 5):      # Boundary line
                        emoLabel = TagMapperDictionary[listStrA]
                    else:
                        emoLabel = 9 # "mixed" # Future Road Map Label
                        break

                if X is None and y is None:
                    X = np.array(listVector)
                    y = np.array([emoLabel])
                else:
                    X = np.vstack( (X, np.array(listVector)) )
                    y = np.hstack( (y, np.array([emoLabel])) )

    assert list(X.shape)[0] == list(y.shape)[0]
    return X, y


def cvredictNBC():
    X, y = GetTrainVectors(globalCSVDataStorePath)
    # print(X.shape)
    # print(y.shape)
    clf.fit(X, y)
    predicted = cross_validation.cross_val_predict(clf, X, y, cv=5)  # better at cv==5
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        print "\n accuracy_score\t", metrics.accuracy_score(y, predicted)
        print "\n precision_score\t", metrics.precision_score(y, predicted)
        print "\n recall_score\t", metrics.recall_score(y, predicted)
        print "\n classification_report:\n\n", metrics.classification_report(y, predicted)
        print "\n confusion_matrix:\n\n", metrics.confusion_matrix(y, predicted)


def mainNBC(emoVector = np.array([[1,0,0,1,0,0,0,0]])):
    X, y = GetTrainVectors(globalCSVDataStorePath)
    # print(X.shape)
    # print(y.shape)
    clf.fit(X, y)

    outList = clf.predict(emoVector)

    outListCat = []
    for anItem in outList:
        outListCat.append(TagMapperList[anItem])
    print("NBC: ",outListCat)

# mainNBC()
# cvredictNBC()