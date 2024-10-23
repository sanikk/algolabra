import time
from decimal import Decimal, getcontext, Rounded, Inexact

from algolabra.fringe.data_structs.doublelinkedlist_mostly_tuples import DoubleLinkedList
from algolabra.common_search_utils.heuristics import heuristics as heuristics
from algolabra.common_search_utils.children import children as children


def fringe_search(start: tuple[int, int], goal: tuple[int, int], citymap: list):
    """
    Implementation for octile maps. No extra data collection or status prints.

    cache dict, node is tuple, children is not

    :param start: starting point (x, y)
    :param goal:  goal point (x, y)
    :param citymap:  map
    :return: cost and route if available
    """
    diag_cost = Decimal('1.4142135623730950488')
    # fmax = 10000000
    fmax = float('inf')


    fringe = DoubleLinkedList(start)

    cache = {start: (0, None)}
    flimit = heuristics(*start, *goal, diag_cost)
    found = False
    found_cost = 0

    while not found and fringe.head:
        fmin = fmax
        # node is a tuple here
        for node in fringe:
            g, parent = cache[node]
            f = g + heuristics(*node, *goal, diag_cost)
            if f > flimit:
                fmin = min(f, fmin)
                continue
            if node == goal:
                found = True
                found_cost = g
                print(f"found {g}")
                break
            for x, y, cost in reversed(children(*node, citymap, diag_cost)):
                child = (x, y)
                g_child = g + cost
                if child in cache:
                    g_cached, parent = cache[child]
                    if g_child >= g_cached:
                        continue
                fringe.add_tail(child)
                cache[child] = g_child, node
            fringe.remove_node(node)
        flimit = fmin
    if found:
        route = [goal]
        while route[-1] != start:
            loc = route[-1]
            route.append(cache[loc][1])
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
