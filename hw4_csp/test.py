#!/usr/bin/env python2
# -*- coding: utf-8 -*-
####################################################
# Summer 2017 COMS 4771 AI Homework 4
# File: test.py
# Name: Qipeng Chen
# UNI:  qc2201
####################################################

import sys, time
from sudoku import Sudoku

START, FINISH = "sudokus_start.txt", "sudokus_finish.txt"

if __name__ == '__main__':

    with open(START, 'r') as start, open(FINISH, 'r') as finish:
        puzzles, solutions = start.readlines(), finish.readlines()
        # puzzles = [puzzles[0], puzzles[1], puzzles[331]]
        # solutions = [solutions[0], solutions[1], solutions[331]]

    for solver in ('AC3', 'BT', "Hybrid"):
        num, solved, total_time = 0, [], 0
        for puzzle, solution in zip(puzzles, solutions):
            num += 1
            game = Sudoku(puzzle)
            start_time = time.clock()
            result = game.solve(solver)
            total_time += time.clock() - start_time
            if game.solve(solver):
                assert str(game) == solution[:-1]
                solved.append(num)
        print "Puzzles solved by {}: {}.".format(solver, solved)
        print "Total solved by {}: {}.".format(solver, len(solved))
        print "Average runtime/puzzle: {}.\n".format(total_time / num)
