#!/usr/bin/env python2
# -*- coding: utf-8 -*-
####################################################
# Summer 2017 COMS 4771 AI Homework 3
# File: problem1.py
# Name: Qipeng Chen
# UNI:  qc2201
####################################################
import sys, csv
import numpy as np

def load_args():
    if len(sys.argv) != 3:
        print "Usage: python", sys.argv[0], "<input file> <output file>."
        exit(1)
    return sys.argv[1], sys.argv[2]


def pla(in_data, max_iter=1000):
    weight = np.zeros(len(in_data[0]))
    out_data = [np.copy(weight)]

    in_data = np.insert(in_data, 2, 1, axis=1)
    for i in xrange(max_iter):
        converged = True
        for sample in in_data:
            feature = sample[:-1]
            label = sample[-1]
            if weight.dot(feature) * label <= 0:
                converged = False
                weight += label * feature
        if converged:
            break
        out_data.append(np.copy(weight))

    return out_data

if __name__ == '__main__':
    in_fname, out_fname = load_args()
    with open(in_fname, 'r') as in_file, open(out_fname, 'w') as out_file:
        out_data = pla(np.array(list(csv.reader(in_file)), dtype=float))
        tmp_writer = csv.writer(out_file, delimiter=',')
        for row in out_data:
            tmp_writer.writerow(row)
