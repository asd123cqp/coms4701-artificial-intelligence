#!/usr/bin/env python2
# -*- coding: utf-8 -*-
####################################################
# Summer 2017 COMS 4771 AI Homework 2
# File: PlayerAI.py
# Name: Qipeng Chen
# UNI:  qc2201
####################################################
import time
import Grid
from BaseAI import BaseAI
from Helper import *

INF = float('inf')
NUM_SET = (2, 4)
TIME_LIMIT = 0.2
MAX_DEPTH = 100

class PlayerAI(BaseAI):
    """docstring for PlayerAI"""
    def __init__(self):
        self.start_time, self.max_depth, self.timeout = 0.0, 0, False

    def getMove(self, grid):
        self.start_time = time.clock()
        self.timeout = False
        best_move = None

        # do iterative deepening
        for self.max_depth in xrange(MAX_DEPTH):
            tmp_best = self.maximize(grid, -INF, INF, 0)[0]
            if self.is_timeout():
                break
            best_move = tmp_best if tmp_best is not None else best_move

        # print "Depth:", depth
        return best_move

    def maximize(self, grid, alpha, beta, depth):

        if self.is_timeout():
            return None, -INF

        if depth > self.max_depth:
            return None, score(grid)

        max_child, max_utility = None, -INF
        for move, child in get_children(grid):

            utility = self.minimize(child, alpha, beta, depth+1)

            if utility > max_utility:
                max_child, max_utility = move, utility

            if max_utility >= beta:
                break

            if max_utility > alpha:
                alpha = max_utility

        return max_child, max_utility


    def minimize(self, grid, alpha, beta, depth):

        if self.is_timeout():
            return -INF

        if depth > self.max_depth:
            return score(grid)

        min_utility = INF
        cells = grid.getAvailableCells()

        for v in NUM_SET:
            for cell in cells:

                child = grid.clone()
                child.setCellValue(cell, v)
                utility = self.maximize(child, alpha, beta, depth+1)[1]

                if utility < min_utility:
                    min_utility = utility

                if min_utility <= alpha:
                    break

                if min_utility < beta:
                    beta = min_utility

        return min_utility


    def is_timeout(self):
        if self.timeout:
            return True
        elif time.clock() - self.start_time > TIME_LIMIT:
            self.timeout = True
            return True
        else:
            return False

if __name__ == '__main__':
    grid, ai = Grid(), PlayerAI()
    for r, row in enumerate([[2048, 1024, 32, 4],
                             [128, 512, 128, 16],
                             [16, 32, 16, 8],
                             [2, 4, 4, 2]]):
        for c, cell in enumerate(row):
            grid.insertTile((r, c), cell)

    print "Available Moves:", grid.getAvailableMoves()
    print ai.getMove(grid)
