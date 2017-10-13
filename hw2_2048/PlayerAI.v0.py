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
from random import randint

class PlayerAI(BaseAI):

    def getMove(self, grid):
        moves = grid.getAvailableMoves()
        return moves[randint(0, len(moves) - 1)] if moves else None
