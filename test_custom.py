from utils import *

from ricochet_robots import *
from search import *

def compare_searchers(problems, header,
                      searchers=[breadth_first_tree_search,
                                 breadth_first_graph_search,
                                 depth_first_graph_search,
                                 iterative_deepening_search,
                                 depth_limited_search,
                                 recursive_best_first_search]):
    def do(searcher, problem):
        p = InstrumentedProblem(problem)
        searcher(p)
        return p

    table = [[name(s)] + [do(s, p) for p in problems] for s in searchers]
    print_table(table, header)

board1 = parse_instance('i1.txt')
board2 = parse_instance('i12.txt')
board3 = parse_instance('instances/i2.txt')
board4 = parse_instance('instances/i3.txt')
board5 = parse_instance('instances/i4.txt')
board6 = parse_instance('instances/i11.txt')

def compare_graph_searchers():
    """Prints a table of search results."""
    compare_searchers(problems=[RicochetRobots(board1), RicochetRobots(board4), RicochetRobots(board6)],
                      header=['Searcher', 'Instance 1', 'Instance 3'])

compare_graph_searchers()
