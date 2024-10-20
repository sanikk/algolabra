import time
from decimal import Decimal, getcontext, Rounded, Inexact

from algolabra.fringe.doublelinkedlist import DoubleLinkedList, Node
from algolabra.common_search_utils.heuristics import heuristics
from algolabra.common_search_utils.children import children



def fringe_search(start: tuple[int, int], goal: tuple[int, int], citymap: list):
    """
    Implementation for octile maps. No extra data collection or status prints.

    :param start: starting point (x, y)
    :param goal:  goal point (x, y)
    :param citymap:  map
    :return: cost and route if available
    """
    diag_cost = Decimal('1.4142135623730950488')
    fmax = 10000000

    start_node = Node(*start, None, None)
    fringe = DoubleLinkedList(start_node)
    cache = [[None for a in line] for line in citymap]

    cache[start_node.y][start_node.x] = 0, None
    flimit = heuristics(start_node, *goal, diag_cost)
    found = False
    found_cost = 0

    while not found and fringe.head:
        fmin = fmax
        for node in fringe:
            g, parent = cache[node.y][node.x]
            f = g + heuristics(node, *goal, diag_cost)
            if f > flimit:
                fmin = min(f, fmin)
                continue
            if node.x == goal[0] and node.y == goal[1]:
                found = True
                found_cost = g
                print(f"found {g}")
                break

            for x, y, cost in reversed(children(node, citymap, diag_cost)):
                g_child = g + cost
                if cache[y][x]:
                    g_cached, parent = cache[y][x]
                    if g_child >= g_cached:
                        continue
                fringe.add_child(x, y, node)
                cache[y][x] = g_child, (node.x, node.y)
            fringe.remove_node(node)
        flimit = fmin
    if found:
        route = [goal]
        while route[-1] != start:
            x,y = route[-1]
            route.append(cache[y][x][1])
        rounded = getcontext().flags[Rounded]
        inexact = getcontext().flags[Inexact]
        return found_cost, route, rounded, inexact

def timed_fringe_search(start, goal, citymap):
    """
    Runner for timed fringe search.
    We setup things here for timing.

    uses time.perf_counter for timing
    + process & thread times

    :param start: (x, y) of start
    :param goal: (x, y) of goal
    :param citymap: a map as container of containers. quack quack.
    :return: cost, timer diffs, route, rounded, inexact
    """
    start_times = [time.perf_counter(), time.process_time(), time.thread_time()]
    cost, route, rounded, inexact = fringe_search(start, goal, citymap)
    end_times = [time.perf_counter(), time.process_time(), time.thread_time()]
    timers = [a - b for a,b in zip(end_times, start_times)]

    return cost, timers, route, rounded, inexact

if __name__=='__main__':
    pass
