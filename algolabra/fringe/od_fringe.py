import time
from decimal import Decimal, getcontext, Rounded, Inexact

from algolabra.fringe.ordered_set_tester import LastUpdatedOrderedDict
from algolabra.common_search_utils.heuristics import heuristics_for_tuples as heuristics
from algolabra.common_search_utils.children import children_with_tuples as children


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

    # visited = 0
    # expanded = 0

    # start_node = Node(*start, None, None)
    # fringe = DoubleLinkedList(start_node)
    fringe = LastUpdatedOrderedDict([(None, None), (start, None)])

    cache = [[None for a in line] for line in citymap]

    cache[start[1]][start[0]] = 0, None
    flimit = heuristics(*start, *goal, diag_cost)
    found = False
    found_cost = 0

    while not found and fringe:
        fmin = fmax
        while node := fringe.peek_last():
        # for node in fringe:
            # print(f"od_fringe {node=}")
            # visited += 1
            g, parent = cache[node[1]][node[0]]
            f = g + heuristics(*node, *goal, diag_cost)
            if f > flimit:
                fmin = min(f, fmin)
                fringe.pass_node()
                continue
            if node[0] == goal[0] and node[1] == goal[1]:
                found = True
                found_cost = g
                print(f"found {g}")
                break

            # fringe.remove_node(node)
            fringe.popitem(last=True)
            # expanded += 1

            for x, y, cost in children(*node, citymap, diag_cost):
                g_child = g + cost
                if cache[y][x]:
                    g_cached, parent = cache[y][x]
                    if g_child >= g_cached:
                        continue
                # fringe.add_child(x, y, node)
                fringe[(x,y)] = None
                cache[y][x] = g_child, (node[0], node[1])
            # fringe.remove_node(node)
        if not found:
            flimit = fmin
            fringe.pass_node()
    if found:
        route = [goal]
        while route[-1] != start:
            x,y = route[-1]
            route.append(cache[y][x][1])
        rounded = getcontext().flags[Rounded]
        inexact = getcontext().flags[Inexact]
        # return found_cost, route, visited, expanded, rounded, inexact
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

    return cost, timers, rounded, inexact

if __name__=='__main__':
    pass
