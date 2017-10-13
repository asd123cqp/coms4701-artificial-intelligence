#!/usr/bin/env python2
# -*- coding: utf-8 -*-
####################################################
# Summer 2017 COMS 4771 AI Homework 1
# Name: Qipeng Chen
# UNI:  qc2201
####################################################
from collections import deque

# Lookup constants
GOAL = (0, 1, 2, 3, 4, 5, 6, 7, 8)
OFFSET = {0: -3, 1: 3, 2: -1, 3: 1}
VALID_MOVES = {0: (1, 3), 1: (1, 2, 3), 2: (1, 2),
               3: (0, 1, 3), 4: (0, 1, 2, 3), 5: (0, 1, 2),
               6: (0, 3), 7: (0, 2, 3), 8: (0, 2)}

class StatesTree(object):
    """docstring for StatesTree"""
    def __init__(self, state, parent, move):
        self.state = state
        self.parent = parent
        self.move = move
        self.done = True if state == GOAL else False
        self.depth = parent.depth + 1 if parent else 0

    def make_children(self):
        zero_idx = self.state.index(0)
        valid_moves = VALID_MOVES[zero_idx]
        children = []
        for m in valid_moves:
            tmp = list(self.state)
            target = zero_idx + OFFSET[m]
            tmp[zero_idx] = tmp[target]
            tmp[target] = 0
            children.append(StatesTree(tuple(tmp), self, m))

        return children

    def back_track(self, path):
        while self.parent is not None:  # back track to find path_to_goal
            path.appendleft(self.move)
            self = self.parent
        return path

    def manh_dist(self):
        dist = 0
        for idx, num in enumerate(self.state):
            if num == 0 or idx == num:
                continue
            dist += abs(idx % 3 - num % 3) + abs(idx / 3 - num / 3)

        return dist

    def print_state(self):
        print " -----"
        for i in xrange(3):
            print "|%d|%d|%d|" %tuple(self.state[i * 3: i * 3 + 3])
        print " -----"

if __name__ == '__main__':
    test = StatesTree([7, 2, 4, 5, 0, 6, 8, 3, 1], None, None)
    print test.manh_dist()
    test = StatesTree([0, 8, 2, 3, 4, 5, 6, 7, 1], None, None)
    print test.manh_dist()
