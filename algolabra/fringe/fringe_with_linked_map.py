from decimal import Decimal, getcontext, Rounded, Inexact

from algolabra.fringe.linked_map_with_values import LinkedMap, Node
from algolabra.common_search_utils.heuristics import heuristics
from algolabra.common_search_utils.children import children

def fringe_search(start: tuple[int, int], goal: tuple[int, int], citymap: list, diag_cost):
    map_size = len(citymap)
    diff = diag_cost - Decimal('2')


    fringe = LinkedMap(start)

    flimit = heuristics(*start, *goal, diff)
    cache = {start: (0, None, flimit)}

    found = False
    found_cost = 0

    while not found and fringe:
        fmin = float('inf')

        for node in fringe:
            g, parent, f = cache[node]
            if not f:
                f = g + heuristics(*node, *goal, diff)
                cache[node] = (g, parent, f)
            if f > flimit:
                fmin = min(f, fmin)
                continue
            if node == goal:
                found = True
                found_cost = g
                break
            for x,y, cost in children(*node, citymap, diag_cost, map_size):
                g_child = g + cost
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
