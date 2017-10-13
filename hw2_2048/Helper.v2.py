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

EMPTY_WEIGHT = 2.7
MAX_WEIGHT = 1.5
# AVG_WEIGHT = 0.5
SMOOTH_WEIGHT = 0.5
MONO_WEIGHT = 1.0
CORNNER_WEIGHT = 2.0

SIZE = 4
MAX_IDX = SIZE - 1
# SIZE_SQURE = 16
CORNER_IDX = set([(0, 0), (0, MAX_IDX), (MAX_IDX, 0), (MAX_IDX, MAX_IDX)])

def get_children(grid, dirs=vecIndex):
    children = []

    for x in dirs:
        gridCopy = grid.clone()

        if gridCopy.move(x):
            children.append((x, gridCopy))

    return children

def old_score(grid):

    empty_cells, max_cell = 0, 0

    for i in xrange(SIZE):
        for j in xrange(SIZE):
            # update empty_cells
            if grid.map[i][j] == 0:
                empty_cells += 1
                continue
            # update max_cell
            if grid.map[i][j] > max_cell:
                max_cell = grid.map[i][j]

    return empty_cells + math.log(max_cell)

def score(grid):

    empty_cells, cell_sum, max_cell, smooth = 0, 0.0, 0, 0
    mono_row, mono_col = [[0] * SIZE] * 2
    max_pos, corner = [], 0

    for i in xrange(SIZE):

        # empty_cells & cell_sum
        for j in xrange(SIZE):
            # update empty_cells
            if grid.map[i][j] == 0:
                empty_cells += 1
                continue
            # update cell_sum & max_cell
            # cell_sum += grid.map[i][j]
            if grid.map[i][j] > max_cell:
                max_cell = grid.map[i][j]
                max_pos = [(i, j)]
            if grid.map[i][j] == max_cell:
                max_pos.append((i, j))

        # smoothness & monotonicity
        # prev_diff_row, prev_diff_col = 0, 0
        for j in xrange(MAX_IDX):
            # update smoothness & monotonicity: left/right  direction
            diff = grid.map[i][j+1] - grid.map[i][j]
            if diff == 0:
                smooth += 1
            else:
                log_diff = math.log(abs(diff), 2)
                smooth -= log_diff
                mono_row[i] += log_diff if diff > 0 else -log_diff

            # update smoothness & monotonicity: up/down direction
            diff = grid.map[j+1][i] - grid.map[j][i]
            if diff == 0:
                smooth += 1
            else:
                log_diff = math.log(abs(diff), 2)
                smooth -= log_diff
                mono_col[i] += log_diff if diff > 0 else -log_diff

    # monotonicity = max(mono[0], mono[1]) + max(mono[2], mono[3])
    # avg = math.log(cell_sum / (SIZE_SQURE - empty_cells), 2)
    max_cell = math.log(max_cell, 2)
    monotonicity = sum(map(abs, mono_row)) + sum(map(abs, mono_col))

    for idx in max_pos:
        if idx in CORNER_IDX:
            corner = max_cell
            break

    return EMPTY_WEIGHT * empty_cells \
           + MAX_WEIGHT * max_cell \
           + SMOOTH_WEIGHT * smooth \
           + MONO_WEIGHT * monotonicity \
           + CORNNER_WEIGHT * corner \
           # + AVG_WEIGHT * avg
