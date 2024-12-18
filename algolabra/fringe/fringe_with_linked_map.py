from decimal import Decimal, getcontext, Rounded, Inexact

from algolabra.fringe.linked_map import LinkedMap
from algolabra.common_search_utils.heuristics import heuristics
from algolabra.common_search_utils.children import children


def fringe_search(start: tuple[int, int], goal: tuple[int, int], citymap: list, diag_cost):
    map_size = len(citymap)
    diff = diag_cost - Decimal('2')

    fringe = LinkedMap(start)
    flimit = heuristics(start[0], start[1], *goal, diff)
    cache = {start: (0, None, flimit)}

    found = False
    found_cost = 0

    while not found and fringe:
        fmin = float('inf')
        for node in fringe:
            data = cache[node]
            if not data[2]:
                data = data[0], data[1], data[0] + heuristics(node[0], node[1], goal[0], goal[1], diff)
                cache[node] = data
            if data[2] > flimit:
                if data[2] < fmin:
                    fmin = data[2]
                continue
            if node == goal:
                found = True
                found_cost = data[0]
                break
            for x,y, cost in children(node[0], node[1], citymap, diag_cost, map_size):
                g_child = data[0] + cost
                if (x,y) in cache:
                    if g_child >= cache[(x,y)][0]:
                        continue
                fringe.add_tail((x,y))
                cache[x,y] = g_child, node, None
            fringe.remove(node)
        flimit = fmin
    if found:
        route = [goal]
        while route[-1] != start:
            loc = route[-1]
            route.append(cache[loc][1])
        rounded = getcontext().flags[Rounded]
        inexact = getcontext().flags[Inexact]
        return found_cost, route, rounded, inexact
