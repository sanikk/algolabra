from decimal import Decimal, getcontext, Rounded, Inexact
from collections import deque

from algolabra.common_search_utils.children import children
from algolabra.common_search_utils.heuristics import heuristics


def fringe_search(start: tuple[int, int], goal: tuple[int, int], citymap: list, diag_cost):
    """
    Rescued this from an abandoned thread. Seems to be the fastest solution.

    :param start:
    :param goal:
    :param citymap:
    :param diag_cost:
    :return:
    """
    map_size = len(citymap)
    diff = diag_cost - Decimal(2)

    now = deque([start])
    later = deque()

    flimit = heuristics(*start, *goal, diff)
    found = False
    found_cost = 0
    cache = {start: (None, 0, flimit)}

    while not found:
        fmin = float('inf')

        while not found and now:
            current = now.popleft()

            data = cache[current]
            if not data[2]:
                cache[current] = data = (data[0], data[1], data[1] + heuristics(*current, *goal, diff))

            if data[2] > flimit:
                fmin = min(data[2], fmin)
                later.append(current)
                continue

            if current == goal:
                found = True
                found_cost = data[1]
                break

            kids = children(*current, citymap, diag_cost, map_size)

            for kid in kids:
                gchild = kid[2] + data[1]
                if (kid[0], kid[1]) not in cache or gchild < cache[kid[0], kid[1]][1]:
                    cache[(kid[0], kid[1])] = current, gchild, None
                    now.appendleft((kid[0], kid[1]))
        flimit = fmin
        if not later:
            break
        now, later = later, now

    if found:
        route = [goal]
        while route[-1] != start:
            route.append(cache[route[-1]][0])
        rounded = getcontext().flags[Rounded]
        inexact = getcontext().flags[Inexact]
        return found_cost, route, rounded, inexact
