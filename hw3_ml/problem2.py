#!/usr/bin/env python2
# -*- coding: utf-8 -*-
####################################################
# Summer 2017 COMS 4771 AI Homework 3
# File: problem2.py
# Name: Qipeng Chen
# UNI:  qc2201
####################################################
import sys, csv
import numpy as np
from problem1 import load_args
from sklearn.preprocessing import StandardScaler

ALPHAS = (0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10)
DEFAULT_MAX = 100

def gradient_descent(X, Y, alpha, max_iter=DEFAULT_MAX):

    m = len(Y)
    beta = np.zeros(len(X[0]))

    for _ in xrange(max_iter):
        f_x = beta.dot(X.T)
        gradient = X.T.dot((f_x - Y)) * alpha / m
        beta -= gradient

    loss = beta.dot(X.T) - Y
    return beta, loss.dot(loss.T) / (2 * m)

if __name__ == '__main__':

    in_fname, out_fname = load_args()
    with open(in_fname, 'r') as in_file, open(out_fname, 'w') as out_file:

        # load data
        tmp_writer = csv.writer(out_file, delimiter=',')
        in_data = np.array(list(csv.reader(in_file)), dtype=float)
        X, Y = in_data[:, :-1], in_data[:, -1]

        # normalization
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X_new = np.insert(X_scaled, 0, 1, axis=1)

        # do gradient_descent() for requested alpha
        for alpha in ALPHAS:
            beta, loss = gradient_descent(X_new, Y, alpha)
            tmp_writer.writerow([alpha, DEFAULT_MAX] + list(beta))

        # find best alpha and number_of_iterations
        best_loss = float('inf')
        for alpha in np.linspace(0.2, 2.0, 10):
            for max_iter in xrange(100, 1001, 100):
                beta, loss = gradient_descent(X_new, Y, alpha, max_iter)
                row = [alpha, max_iter] + list(beta)
                if loss < best_loss:
                    best_loss, best_row = loss, row

        # write best to file
        tmp_writer.writerow(best_row)
