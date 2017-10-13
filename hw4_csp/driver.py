#!/usr/bin/env python2
# -*- coding: utf-8 -*-
####################################################
# Summer 2017 COMS 4771 AI Homework 4
# File: driver.py
# Name: Qipeng Chen
# UNI:  qc2201
####################################################

import sys
from sudoku import Sudoku

FILE_NAME = "output.txt"

if __name__ == '__main__':

    # check args num
    if len(sys.argv) not in (2, 3):
        print "Usage: python driver.py <input_string> [solver(default:bt)]."
        exit(1)

    # run solver
    board = Sudoku(sys.argv[1])
    board.solve('bt' if len(sys.argv) == 2 else sys.argv[2])
    with open(FILE_NAME, 'w') as f:
        f.write(str(board))
