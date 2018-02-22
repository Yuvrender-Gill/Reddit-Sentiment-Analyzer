from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import Imputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import confusion_matrix
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import f_classif
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import LogisticRegression
from scipy import stats
import numpy as np
import argparse
import sys
import os
import numpy as np
import sys
import argparse
import os
import json
import csv
import warnings


def accuracy( C ):
    ''' Compute accuracy given Numpy array confusion matrix C. Returns a floating point value '''
    num = 0
    for i in range(len(C)):
        num +=  C[i][i]
    denom = 0
    for i in range(len(C)):
        for j in range(len(C)):
            denom += C[i][j]

    return num/denom if denom != 0 else 0


def recall( C ):
    ''' Compute recall given Numpy array confusion matrix C. Returns a list of floating point values '''
    denom = 0
    for i in range(len(C)):
        for j in range(len(C)):
            denom += C[i][j]
    lst = [C[i][i]/denom if denom != 0 else 0 for i in range(len(C))]
    return lst


def precision( C ):
    ''' Compute precision given Numpy array confusion matrix C. Returns a list of floating point values '''
    denom0, denom1, denom2, denom3 = 0, 0, 0, 0
    for i in range(4):
        denom0 += C[i][0]
    for i in range(4):
        denom1 += C[i][1]
    for i in range(4):
        denom2 += C[i][2]
    for i in range(4):
        denom3 += C[i][3]
    ret_tuple = (C[0][0] / denom0 if denom0 != 0 else 0, C[1][1] / denom1 if denom1 != 0 else 0,
                 C[2][2] / denom2 if denom2 != 0 else 0, C[3][3] / denom3 if denom3 != 0 else 0)
    return ret_tuple
    

def class31(filename):
    ''' This function performs experiment 3.1
    
    Parameters
       filename : string, the name of the npz file from Task 2

    Returns:      
       X_train: NumPy array, with the selected training features
       X_test: NumPy array, with the selected testing features
       y_train: NumPy array, with the selected training classes
       y_test: NumPy array, with the selected testing classes
       i: int, the index of the supposed best classifier
    '''
    a = np.load(filename)
    d = dict(zip(("d"), (a[k] for k in a)))
    data_array = d["d"]
    np.random.shuffle(data_array)
    # Split 173 + 1
    # Clean the nan values from data
    imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
    imp.fit(data_array)
    imp_data = imp.transform(data_array)
    # split data
    X, y = imp_data[:, :-1], imp_data[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, train_size=0.80)

    iBest = 0
    # Use classifier 1=============================
    clf1 = SVC(kernel='linear')
    clf1.fit(X_train, y_train)
    prediction_1 = clf1.predict(X_test)
    # Use classifier 2=============================
    clf2 = SVC(gamma=2)
    clf2.fit(X_train, y_train)
    prediction_2 = clf2.predict(X_test)
    # Use classifier 3=============================
    clf3 = RandomForestClassifier(n_estimators=10, max_depth=5)
    clf3.fit(X_train, y_train)
    prediction_3 = clf3.predict(X_test)
    # Use classifier 4=============================
    clf4 = MLPClassifier(alpha=0.05)
    clf4.fit(X_train, y_train)
    prediction_4 = clf4.predict(X_test)
    # Use classifier 5=============================
    clf5 = AdaBoostClassifier()
    clf5.fit(X_train, y_train)
    prediction_5 = clf5.predict(X_test)

    #Obtaining the confustion matrix

    matrix1 = confusion_matrix(y_test, prediction_1)
    matrix2 = confusion_matrix(y_test, prediction_2)
    matrix3 = confusion_matrix(y_test, prediction_3)
    matrix4 = confusion_matrix(y_test, prediction_4)
    matrix5 = confusion_matrix(y_test, prediction_5)

    # Obtaining best classifier

    A1 = accuracy(matrix1)
    R1 = recall(matrix1)
    P1 = precision(matrix1)

    A2 = accuracy(matrix2)
    R2 = recall(matrix2)
    P2 = precision(matrix2)

    A3 = accuracy(matrix3)
    R3 = recall(matrix3)
    P3 = precision(matrix3)

    A4 = accuracy(matrix4)
    R4 = recall(matrix4)
    P4 = precision(matrix4)

    A5 = accuracy(matrix5)
    R5 = recall(matrix5)
    P5 = precision(matrix5)

    #csv vectors
    csv1 = [1, A1] + list(R1) + list(P1) + list(matrix1[0]) + list(matrix1[1]) + list(matrix1[2]) + list(matrix1[3])
    csv2 = [2, A2] + list(R2) + list(P2) + list(matrix2[0]) + list(matrix2[1]) + list(matrix2[2]) + list(matrix2[3])
    csv3 = [3, A3] + list(R3) + list(P3) + list(matrix3[0]) + list(matrix3[1]) + list(matrix3[2]) + list(matrix3[3])
    csv4 = [4, A4] + list(R4) + list(P4) + list(matrix4[0]) + list(matrix4[1]) + list(matrix4[2]) + list(matrix4[3])
    csv5 = [5, A5] + list(R5) + list(P5) + list(matrix5[0]) + list(matrix5[1]) + list(matrix5[2]) + list(matrix5[3])

    # Write csv file
    with open("a1_3.1(11).csv", 'w') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(csv1)
        wr.writerow(csv2)
        wr.writerow(csv3)
        wr.writerow(csv4)
        wr.writerow(csv5)
    acc_list = [A1, A2, A3, A4, A5]
    iBest = acc_list.index(max(acc_list)) + 1

    return (X_train, X_test, y_train, y_test,iBest)


def class32(nX_train, nX_test, ny_train, ny_test,iBest):
    ''' This function performs experiment 3.2
    
    Parameters:
       X_train: NumPy array, with the selected training features
       X_test: NumPy array, with the selected testing features
       y_train: NumPy array, with the selected training classes
       y_test: NumPy array, with the selected testing classes
       i: int, the index of the supposed best classifier (from task 3.1)  

    Returns:
       X_1k: numPy array, just 1K rows of X_train
       y_1k: numPy array, just 1K rows of y_train
   '''

    acc_list = []
    if iBest == 1:
        # Use classifier 1=============================
        clf = SVC(kernel='linear')
        clf.fit(nX_train, ny_train)
        prediction = clf.predict(nX_test)
        matrix = confusion_matrix(ny_test, prediction)
        A = accuracy(matrix)
    elif iBest == 2:
        # Use classifier 2=============================
        clf = SVC(gamma=2)
        clf.fit(nX_train, ny_train)
        prediction = clf.predict(nX_test)
        matrix = confusion_matrix(ny_test, prediction)
        A = accuracy(matrix)
    elif iBest == 3:
        # Use classifier 3=============================
        clf = RandomForestClassifier(n_estimators=10, max_depth=5)
        clf.fit(nX_train, ny_train)
        prediction = clf.predict(nX_test)
        matrix = confusion_matrix(ny_test, prediction)
        A = accuracy(matrix)
    elif iBest == 4:
        # Use classifier 4=============================
        clf = MLPClassifier(alpha=0.05)
        clf.fit(nX_train, ny_train)
        prediction = clf.predict(nX_test)
        matrix = confusion_matrix(ny_test, prediction)
        A = accuracy(matrix)
    else:
        # Use classifier 5=============================
        clf = AdaBoostClassifier()
        clf.fit(nX_train, ny_train)
        prediction = clf.predict(nX_test)
        matrix = confusion_matrix(ny_test, prediction)
        A = accuracy(matrix)

    acc_list.append(A)

    with open("temp.csv", 'a') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(acc_list)

    return nX_train[0:int(len(nX_train)), :], ny_train[0:int(len(ny_train))]


def class33(X_train, X_test, y_train, y_test, i, X_1k, y_1k):
    ''' This function performs experiment 3.3
    
    Parameters:
       X_train: NumPy array, with the selected training features
       X_test: NumPy array, with the selected testing features
       y_train: NumPy array, with the selected training classes
       y_test: NumPy array, with the selected testing classes
       i: int, the index of the supposed best classifier (from task 3.1)  
       X_1k: numPy array, just 1K rows of X_train (from task 3.2)
       y_1k: numPy array, just 1K rows of y_train (from task 3.2)
    '''
    # se = [5, 10, 20, 30, 40, 50]
    # for k in se:
    #     selector = SelectKBest(f_classif, k)
    #     X_new = selector.fit_transform(X_train, y_train)
    #     pp = selector.pvalues
    #     pipeline = Pipeline([('kbest', selector), ('lr', LogisticRegression())])
    #     grid_search = GridSearchCV(pipeline, {'kbest__k': [1, 2, 3, 4], 'lr__C': np.logspace(-10, 10, 5)})
    #     grid_search.fit(X, y)
    #     _
    #     print(pp)


def class34( filename, i ):
    ''' This function performs experiment 3.4
    
    Parameters
       filename : string, the name of the npz file from Task 2
       i: int, the index of the supposed best classifier (from task 3.1)  
        '''
    kf = KFold(n_splits=5, shuffle=True)




def main(args):
    file_name = args.input
    class31_array = class31(file_name)

    train = ((len(class31_array[0]) * 0.025) / 0.8, (len(class31_array[0]) * 0.125) / 0.8, (len(class31_array[0]) * 0.25) / 0.8,
             (len(class31_array[0]) * 0.375) / 0.8, (len(class31_array[0]) * 0.5) / 0.8)
    test = ((len(class31_array[1]) * 0.025) / 0.2, (len(class31_array[1]) * 0.125) / 0.2, (len(class31_array[1]) * 0.25) / 0.2,
            (len(class31_array[1]) * 0.375) / 0.2, (len(class31_array[1]) * 0.5) / 0.2)

    for i in range(5):
        ny_train = class31_array[2][0:int(train[i])]
        nX_train = class31_array[0][0:int(train[i]), :]
        ny_test = class31_array[3][0:int(test[i])]
        nX_test = class31_array[1][0:int(test[i]), :]
        class32_array = class32(nX_train, nX_test, ny_train,
                                ny_test, 1)
    # index = 0
   # class33(class31_array[0], class31_array[1], class31_array[2], class31_array[3],
    #        class31_array[4], class32_array[0], class32_array[1])
    # class34(file_name, index)
    csv1 = []
    with open("temp.csv") as myfile:
        reader = csv.reader(myfile, delimiter=',')
        for row in reader:
            csv1.append(row[0])
    with open("a1_3.2(1000).csv", 'w') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(csv1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process each .')
    parser.add_argument("-i", "--input", help="the input npz file from Task 2", required=True)
    args = parser.parse_args()

    main(args)
    # TODO : complete each classification experiment, in sequence.
