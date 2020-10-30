
from ricochet_robots import *
from search import astar_search, breadth_first_tree_search, \
    depth_first_tree_search, greedy_search

board = parse_instance("i12.txt")
problem = RicochetRobots(board)
s0 = RRState(board)
