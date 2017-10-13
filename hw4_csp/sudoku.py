#!/usr/bin/env python2
# -*- coding: utf-8 -*-
####################################################
# Summer 2017 COMS 4771 AI Homework 4
# File: game.py
# Name: Qipeng Chen
# UNI:  qc2201
####################################################

from collections import deque
from heapq import heappush, heappop

# all available indexes
INDEXES = [(i, j) for i in range(9) for j in range(9)]

# lookup table to get all cells in the same row/column/box
ARC_LOOKUP = [[None] * 9 for _ in range(9)]

# helper function
def get_arcs(idx):
    '''Get the index of all other cells in the same row, column or box'''
    if ARC_LOOKUP[idx[0]][idx[1]] is None:
        row = [(i, idx[1]) for i in range(idx[0]) + range(idx[0]+1, 9)]
        col = [(idx[0], j) for j in range(idx[1]) + range(idx[1]+1, 9)]
        box = [(i, j) for i in range(idx[0]/3*3, idx[0]) + \
                               range(idx[0]+1, idx[0]/3*3+3) \
                      for j in range(idx[1]/3*3, idx[1]) + \
                               range(idx[1]+1, idx[1]/3*3+3)]

        ARC_LOOKUP[idx[0]][idx[1]] = set(row + col + box)

    return ARC_LOOKUP[idx[0]][idx[1]]


# main Sudoku class
class Sudoku(object):
    """The Sudoku Class"""
    def __init__(self, puzzle=None):
        self.board = None
        self.rv, self.rv_lookup = [], {}
        self.domain = [[None] * 9 for _ in range(9)]
        if puzzle is not None:
            self.set_state(puzzle)

    def get(self, idx):
        '''Get value for a cell'''
        return self.board[idx[0]][idx[1]]

    def set_val(self, idx, val):
        '''Set value for a cell'''
        self.board[idx[0]][idx[1]] = val         # set value
        self.domain[idx[0]][idx[1]] = set([val]) # set domain
        if idx in self.rv_lookup:
            self.rv_lookup[idx][1] = None        # clean up rv queue
            del self.rv_lookup[idx]              # clean up lookup table

    def dom(self, idx):
        '''Get domain for a cell'''
        return self.domain[idx[0]][idx[1]]

    def set_dom(self, idx, dom):
        '''Set domain for a cell'''
        self.domain[idx[0]][idx[1]] = dom
        rv_entry = [len(dom), idx]
        if idx in self.rv_lookup:
            self.rv_lookup[idx][1] = None
        self.rv_lookup[idx] = rv_entry
        heappush(self.rv, rv_entry)

    def set_state(self, state):
        '''Set current board state with a puzzle string'''
        self.board = [[int(c) for c in state[i*9:(i+1)*9]] for i in range(9)]
        self.rv, self.rv_lookup = [], {}
        for idx in INDEXES:
            if self.get(idx) == 0:
                used_vals = set([self.get(tgt) for tgt in get_arcs(idx)])
                self.set_dom(idx, set(range(1, 10)) - used_vals)
            else:
                self.domain[idx[0]][idx[1]] = set([self.get(idx)])

    def ac3(self):
        '''Maintain arc consistency using AC-3'''
        arcs = deque([(idx, tgt) for idx in INDEXES for tgt in get_arcs(idx)])
        while arcs:
            (src, tgt) = arcs.pop()
            if src != tgt and self.__revised__(src, tgt):
                if not self.dom(src):
                    return False
                arcs.extend([(nei, src) for nei in get_arcs(src) - set([tgt])])
        return True

    def __revised__(self, src, tgt):
        '''Helper function for ac3'''
        deleted = set()
        for x in self.dom(src):
            satisfied = False
            for y in self.dom(tgt):
                if x != y:
                    satisfied = True
                    break
            if not satisfied:
                deleted.add(x)
        if deleted:
            self.set_dom(src, self.dom(src) - deleted)
            return True
        return False

    def ac3_solver(self):
        '''Try to solve the puzzle using AC-3'''
        self.ac3()
        while self.rv:
            rv, idx = heappop(self.rv)
            if idx is None: # dummy entry -> ignore
                continue
            if rv > 1:
                if self.ac3(): # no more progress using ac3 -> failed to solve
                    return False
                continue # new inconsistency found -> can try again
            self.set_val(idx, self.dom(idx).pop())
        return True


    def __fwd_checking__(self, idx, val):
        '''Helper function for bt_search'''
        changed = []
        for tgt in get_arcs(idx):
            tgt_dom = self.dom(tgt)
            if val in tgt_dom: # target domain contains newly added value
                if len(tgt_dom) == 1: # inevitable failure detected
                    return False, changed
                tgt_dom.remove(val) # reduce target domain
                self.set_dom(tgt, tgt_dom)
                changed.append(tgt)
        return True, changed

    def bt_solver(self):
        '''Try to solve the puzzle using backtracking search'''

        # retrieve mrv
        idx = None
        while self.rv:
            rv, idx = heappop(self.rv)
            if idx is not None: # dummy entry -> ignore
                break

        # base case reached: no more remaining variable -> solved!
        if not self.rv and idx is None:
            return True

        # make a guess
        old_dom = self.dom(idx)
        for val in old_dom:
            self.set_val(idx, val)
            consistent, changed = self.__fwd_checking__(idx, val)
            if consistent and self.bt_solver(): # it works! -> solved!
                return True
            for tgt in changed: # reset changes done by forward checking
                self.dom(tgt).add(val)
                self.set_dom(tgt, self.dom(tgt))

        # all value in domain failed -> need to reset & backtrack
        self.board[idx[0]][idx[1]] = 0 # reset value
        self.set_dom(idx, old_dom)     # reset domain
        return False

    def hybrid_solver(self):
        '''Try to solve the puzzle using backtracking search + AC-3'''
        # print sum([r[0] if r[1] is not None else 0 for r in self.rv])
        if self.ac3_solver():
            return True
        # print sum([r[0] if r[1] is not None else 0 for r in self.rv])
        return self.bt_solver()

    def solve(self, solver='bt'):
        solver = solver.lower()
        if solver not in ['ac3', 'bt', 'hybrid']:
            raise NameError("Valid solvers include `ac3`, `bt` and 'hybrid'.")
        return getattr(self, solver + "_solver")()

    def print_board(self):
        if self.board is not None:
            print "–  0 1 2 3 4 5 6 7 8\n|"
            for i, row in enumerate(self.board):
                print i, "", " ".join(str(c) for c in row)

    def __str__(self):
        return ''.join(str(self.get(i)) for i in INDEXES)

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    a = "003020600900305001001806400008102900700000008006708200002609500800203009005010300"
    b = "483921657967345821251876493548132976729564138136798245372689514814253769695417382"
    c = "000100702030950000001002003590000301020000070703000098800200100000085060605009000"
    d = "956138742237954816481672953594867321128593674763421598879246135312785469645319287"
    e = "800000000003600000070090200050007000000045700000100030001000068008500010090000400"
    f = "812753649943682175675491283154237896369845721287169534521974368438526917796318452"
    test = Sudoku(e)
    test.print_board()
    print "\nIs solved:", test.solve('hybrid')
    test.print_board()
    print "Match solution:", str(test) == f
