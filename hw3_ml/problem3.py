#!/usr/bin/env python2
# -*- coding: utf-8 -*-
####################################################
# Summer 2017 COMS 4771 AI Homework 3
# File: problem3.py
# Name: Qipeng Chen
# UNI:  qc2201
####################################################
import sys, csv
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import svm, linear_model, neighbors, tree, ensemble
from problem1 import load_args

MODELS = {
    "svm_linear": {
        "base": svm.SVC(kernel='linear'),
        "params": {
            'C': (0.1, 0.5, 1, 5, 10, 50, 100)
        }
    },
    "svm_polynomial": {
        "base": svm.SVC(kernel='poly'),
        "params": {
            'C': (0.1, 1, 3),
            'degree': (4, 5, 6),
            'gamma': (0.1, 0.5)
        }
    },
    "svm_rbf": {
        "base": svm.SVC(kernel='rbf'),
        "params": {
            'C': (0.1, 0.5, 1, 5, 10, 50, 100),
            'gamma': (0.1, 0.5, 1, 3, 6, 10)
        }
    },
    "logistic": {
        "base": linear_model.LogisticRegression(),
        "params": {
            'C': (0.1, 0.5, 1, 5, 10, 50, 100)
        }
    },
    "knn": {
        "base": neighbors.KNeighborsClassifier(),
        "params": {
            'n_neighbors': range(1, 51),
            'leaf_size': range(5, 61, 5)
        }
    },
    "decision_tree": {
        "base": tree.DecisionTreeClassifier(),
        "params": {
            'max_depth': range(1, 50),
            'min_samples_split': range(2, 11)
        }
    },
    "random_forest": {
        "base": ensemble.RandomForestClassifier(),
        "params": {
            'max_depth': range(1, 50),
            'min_samples_split': range(2, 11)
        }
    }
}

MODEL_ORDER = ("svm_linear", "svm_polynomial", "svm_rbf",
               "logistic", "knn", "decision_tree", "random_forest")

def classify(base, grid, data):
    X_train, X_test, y_train, y_test = data
    model = GridSearchCV(estimator=base, param_grid=grid, cv=5)
    model.fit(X_train, y_train)
    return [model.score(X_train, y_train), model.score(X_test, y_test)]

if __name__ == '__main__':

    in_fname, out_fname = load_args()
    with open(in_fname, 'rU') as in_file, open(out_fname, 'w') as out_file:
        in_data = np.array(list(csv.reader(in_file))[1:], dtype=float)
        data = train_test_split(in_data[:, :-1], in_data[:, -1],
                                test_size=0.4, random_state=2201)

        tmp_writer = csv.writer(out_file, delimiter=',')
        for m in MODEL_ORDER:
            print "\nStart fitting %s..." %(m)
            ret = classify(MODELS[m]["base"], MODELS[m]["params"], data)
            print "Best_score: %f. Test_score: %f.\nDone!" %(ret[0], ret[1])
            tmp_writer.writerow([m] + ret)
            out_file.flush()

    print "\nAll done!\n"
