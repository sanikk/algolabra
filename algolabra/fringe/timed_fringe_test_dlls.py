import time
from decimal import Decimal

from doublelinkedlist import DoubleLinkedList, Node
from heuristics import heuristics
from children import children
from doublelinkedlist_version import DoubleLinkedList as DLL2, Node as N2
from doublelinkedlist_version import DoubleLinkedListTwo as DLL3


def fringe_search(start: tuple[int, int], goal: tuple[int, int], citymap: list):
    """
    Implementation for octile maps. No extra data collection or status prints.

    :param start: starting point (x, y)
    :param goal:  goal point (x, y)
    :param citymap:  map
    :return: cost and route if available
    """
    diag_cost = Decimal(2).sqrt()
    fmax = 10000000

    start_node = N2(*start, None, None)
    fringe = DLL2(start_node)

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

            for x, y, cost in children(node, citymap, diag_cost):
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
        return found_cost, route

def fringe_search_with_new_dll(start: tuple[int, int], goal: tuple[int, int], citymap: list):
    """
    Implementation for octile maps. No extra data collection or status prints.

    :param start: starting point (x, y)
    :param goal:  goal point (x, y)
    :param citymap:  map
    :return: cost and route if available
    """
    diag_cost = Decimal(2).sqrt()
    fmax = 10000000

    start_node = N2(*start, None, None)
    fringe = DLL3(start_node)

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

            for x, y, cost in children(node, citymap, diag_cost):
                g_child = g + cost
                if cache[y][x]:
                    g_cached, parent = cache[y][x]
                    if g_child >= g_cached:
                        continue
                fringe.add_child(x, y)
                cache[y][x] = g_child, (node.x, node.y)
            fringe.remove_node(node)
        flimit = fmin
    if found:
        route = [goal]
        while route[-1] != start:
            x,y = route[-1]
            route.append(cache[y][x][1])
        return found_cost, route


def timed_fringe_search(start, goal, citymap) -> tuple[int, list, list]:
    """
    Runner for timed fringe search.
    We setup things here for timing.

    uses time.perf_counter for timing
    + process & thread times

    :param start: (x, y) of start
    :param goal: (x, y) of goal
    :param citymap: a map as container of containers. quack quack.
    :return: cost, timer diffs, route
    """

    start_times = [time.perf_counter(), time.process_time(), time.thread_time()]
    cost, route = fringe_search(start, goal, citymap)
    end_times = [time.perf_counter(), time.process_time(), time.thread_time()]
    timers = [a - b for a,b in zip(end_times, start_times)]
    print("fringe search")
    print(f"{cost=}")
    print(f"{timers=}")
    print(f"{route=}")

    start_times = [time.perf_counter(), time.process_time(), time.thread_time()]
    cost, route = fringe_search_with_new_dll(start, goal, citymap)
    end_times = [time.perf_counter(), time.process_time(), time.thread_time()]
    timers = [a - b for a, b in zip(end_times, start_times)]
    print("fringe search with new dll")
    print(f"{cost=}")
    print(f"{timers=}")
    print(f"{route=}")

    return cost, timers, route


if __name__=='__main__':
    from read_files import read_map
    le_map = read_map("Boston_0_512.map")
    # 6	Boston_0_512.map	512	512	487	85	489	109	27.31370850
    timed_fringe_search((487, 85), (489, 109), le_map)
    pass
