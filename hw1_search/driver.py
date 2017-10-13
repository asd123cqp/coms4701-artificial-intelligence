#!/usr/bin/env python2
# -*- coding: utf-8 -*-
####################################################
# Summer 2017 COMS 4771 AI Homework 1
# Name: Qipeng Chen
# UNI:  qc2201
####################################################
import sys
from game import Game

SOLVER = ['bfs', 'dfs', 'ast']
FILE_NAME = "output.txt"

if __name__ == '__main__':

    # check args num
    if len(sys.argv) != 3:
        print "Usage: python driver.py <method> <board>."
        exit(1)

    # get argv
    solver = sys.argv[1]
    init_state = map(int, sys.argv[2].split(','))

    # check if initial_state is valid
    if len(set(init_state)) != 9 or \
       min(init_state) != 0 or max(init_state) != 8:
        print "Invalid initial state!"
        exit(1)

    # run solver
    sys.stdout = open(FILE_NAME, "w")
    g = Game(init_state)
    g.solve(solver)
    sys.stdout.close()
