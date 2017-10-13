#!/usr/bin/env python2
# -*- coding: utf-8 -*-
####################################################
# Summer 2017 COMS 4771 AI Homework 1
# Name: Qipeng Chen
# UNI:  qc2201
####################################################
import sys, time, resource
from heapq import heappush, heappop
from collections import deque
from Queue import Queue
from statestree import StatesTree

# Lookup constants
MOVES = ("Up", "Down", "Left", "Right")

# Helper function to update max_ram_usage
def update_max_ram(prev_max):
    cur = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000.0
    return max(prev_max, cur)

class Game(object):
    """docstring for Game"""

    def __init__(self, init_state):
        self.init_state = tuple(init_state)

    def solve(self, solver, trim_path=False):
        '''
        Solve the game from initial state.
        solver - Which method(bfs, dfs or ast) to use
        trim_path - If you want to trim long path (len > 30) or not
        '''
        # Initialize ret - the array of desired values
        ret = [deque(), # ret[0] - path_to_goal
               0,       # ret[1] - int, nodes_expanded
               0,       # ret[2] - int, search_depth
               0,       # ret[3] - int, max_search_depth
               0]       # ret[4] - int, max_ram_usage
        running_time = time.time()
        ret = getattr(self, solver)(ret)
        running_time = time.time() - running_time

        if ret is None:
            print "Failed to solve", self.init_state, "with", arg
            return

        # print result
        path = [MOVES[m] for m in ret[0]]
        if trim_path and len(path) > 30: # trim long path
            path = path[:15] + ["......"] + path[-15:]
        print "path_to_goal:", path
        print "cost_of_path:", len(ret[0])
        print "nodes_expanded:", ret[1]
        print "search_depth:", ret[2]
        print "max_search_depth:", ret[3]
        print "running_time: %.8f" %(running_time)
        print "max_ram_usage: %.8f"  %(ret[4])

    def bfs(self, ret):
        '''Solve the game using Breadth-First Search'''
        frontier, explored = Queue(), set([self.init_state])
        frontier.put(StatesTree(self.init_state, None, None))

        while not frontier.empty():
            cur = frontier.get()

            # found solution!
            if cur.done:
                ret[2] = cur.depth     # set search_depth
                cur.back_track(ret[0]) # back track to recover path_to_goal
                return ret

            ret[1] += 1 # set nodes_expanded
            has_valid_child = False # if added at least one child to queue
            for child in cur.make_children():
                if child.state not in explored:
                    frontier.put(child)
                    explored.add(child.state)
                    has_valid_child = True

            # set max_search_depth & max_ram_usage
            ret[3] = max(ret[3], cur.depth + 1) if has_valid_child else ret[3]
            ret[4] = update_max_ram(ret[4])

        return None

    def dfs(self, ret):
        '''Solve the game using Depth-First Search'''
        frontier, explored = deque(), set([self.init_state])
        frontier.append(StatesTree(self.init_state, None, None))

        while frontier:
            cur = frontier.pop()

            # found solution!
            if cur.done:
                ret[2] = cur.depth     # set search_depth
                cur.back_track(ret[0]) # back track to recover path_to_goal
                return ret

            ret[1] += 1 # set nodes_expanded
            has_valid_child = False # if added at least one child to stack
            for child in cur.make_children()[::-1]:
                if child.state not in explored:
                    frontier.append(child)
                    explored.add(child.state)
                    has_valid_child = True

            # set max_search_depth & max_ram_usage
            ret[3] = max(ret[3], cur.depth + 1) if has_valid_child else ret[3]
            ret[4] = update_max_ram(ret[4])

        return None

    def ast(self, ret):
        '''Solve the game using A-Star Search'''
        root_entry = [0, StatesTree(self.init_state, None, None)]
        frontier, explored = [root_entry], set([])
        heap_finder = {self.init_state: root_entry}

        while frontier:
            dist, cur = heappop(frontier)
            if cur is None: # the node is deleted
                continue
            del heap_finder[cur.state]

            # found solution!
            if cur.done:
                # ret[1] = len(explored)
                ret[2] = cur.depth     # set search_depth
                cur.back_track(ret[0]) # back track to recover path_to_goal
                return ret

            ret[1] += 1     # set nodes_expanded
            has_valid_child = False  # if added at least one child to heap
            explored.add(cur.state)
            for child in cur.make_children():
                if child.state in explored:
                    continue
                new_dist = child.depth + child.manh_dist()
                if child.state in heap_finder: # already in heap: decreaseKey
                    old_entry = heap_finder[child.state]
                    if old_entry[0] <= new_dist: # old one is better: skip
                        continue
                    else:
                        old_entry[1] = None # mark as deleted
                new_entry = [new_dist, child]
                heappush(frontier, new_entry)
                heap_finder[child.state] = new_entry
                has_valid_child = True

            # set max_search_depth & max_ram_usage
            # ret[1] += 1 if has_valid_child else 0     # set nodes_expanded
            ret[3] = max(ret[3], cur.depth + 1) if has_valid_child else ret[3]
            ret[4] = update_max_ram(ret[4])

        return None


if __name__ == '__main__':
    testcases = [[3, 1, 2, 0, 4, 5, 6, 7, 8],
                 [1, 2, 5, 3, 4, 0, 6, 7, 8],
                 [6, 1, 8, 4, 0, 2, 7, 3, 5],
                 [8, 6, 4, 2, 1, 3, 5, 7, 0]]

    for t in testcases:
        print "----- Solving", t, "-----"
        test = Game(t)
        print "----- Using DFS -----"
        # test.solve('dfs', True)
        print "----- Using BFS -----"
        # test.solve('bfs')
        print "----- Using A-Star -----"
        test.solve('ast')
        print "----- Done! -----\n"
