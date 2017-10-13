#!/usr/bin/env python2
# -*- coding: utf-8 -*-
####################################################
# Summer 2017 COMS 4771 AI Homework 2
# File: Helper.py
# Name: Qipeng Chen
# UNI:  qc2201
####################################################
import math
from Grid import Grid, vecIndex

EMPTY_WEIGHT = 3.0
MAX_WEIGHT = 1.0
SMOOTH_WEIGHT = 0.5
MONO_WEIGHT = 0.5
CORNNER_WEIGHT = 3.0

SIZE = 4
MAX_IDX = SIZE - 1
CORNER_IDX = set([(0, 0), (0, MAX_IDX), (MAX_IDX, 0), (MAX_IDX, MAX_IDX)])

def get_children(grid, dirs=vecIndex):
    children = []

    for x in dirs:
        gridCopy = grid.clone()

        if gridCopy.move(x):
            children.append((x, gridCopy))

    return children


def score(grid):

    empty_cells, max_cell, smooth = 0, 0, 0.0
    mono_row, mono_col = [[0.0] * SIZE] * 2
    max_pos, corner = [], 0

    for i in xrange(SIZE):

        # empty_cells & cell_sum
        for j in xrange(SIZE):
            # update empty_cells
            if grid.map[i][j] == 0:
                empty_cells += 1
                continue
            # update cell_sum & max_cell
            if grid.map[i][j] > max_cell:
                max_cell = grid.map[i][j]
                max_pos = [(i, j)]
            if grid.map[i][j] == max_cell:
                max_pos.append((i, j))
        # smoothness & monotonicity
        for j in xrange(MAX_IDX):
            # update smoothness & monotonicity: left/right  direction
            diff = grid.map[i][j+1] - grid.map[i][j]
            mono_row[i] += 1 if diff > 0 else -1
            smooth += 1 if diff == 0 else -math.log(abs(diff), 2)

            # update smoothness & monotonicity: up/down direction
            diff = grid.map[j+1][i] - grid.map[j][i]
            mono_col[i] += 1 if diff > 0 else -1
            smooth += 1 if diff == 0 else -math.log(abs(diff), 2)

    max_cell = math.log(max_cell, 2)
    monotonicity = sum(map(abs, mono_row)) + sum(map(abs, mono_col)) * max_cell

    for idx in max_pos:
        if idx in CORNER_IDX:
            corner = max_cell
            break

    return EMPTY_WEIGHT * empty_cells \
           + MAX_WEIGHT * max_cell \
           + SMOOTH_WEIGHT * smooth \
           + MONO_WEIGHT * monotonicity \
           + CORNNER_WEIGHT * corner
