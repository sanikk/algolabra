from decimal import Decimal, getcontext, Rounded, Inexact
from collections import deque

from algolabra.common_search_utils.children import children
from algolabra.common_search_utils.heuristics import old_heuristics as heuristics


"""
Version made in tandem with ChatGPT. This took some back and forth.

End result is about the same as my abandoned fast_version_with_deque. 
Neither is satisfactory on long paths, larger maps.

"""


def fringe_search(start: tuple[int, int], goal: tuple[int, int], citymap: list, diag_cost):
    map_size = len(citymap)

    now = deque([start])
    later = deque()
    diff = diag_cost - 1

    flimit = heuristics(*start, *goal, diff)
    found = False
    found_cost = 0
    cache = {start: (0, None)}

    while not found:
        fmin = float('inf')

        while not found and now:
            current = now.popleft()

            g, parent = cache[current]
            f = g + heuristics(*current, *goal, diff)

            if f > flimit:
                fmin = min(f, fmin)
                later.append(current)
                continue

            if current == goal:
                found_cost = g
                found = True
                break

            kids = children(*current, citymap, diag_cost, map_size)

            kids_left = []
            for kid in kids:
                tup = (kid[0], kid[1])
                gchild = kid[2] + g
                if gchild < cache.get(tup, (float('inf'), None))[0]:
                    cache[tup] = gchild, current
                    kids_left.append(tup)
            now.extend(kids_left)
        flimit = fmin
        if not later:
            break
        to_be = now
        now = later
        later = to_be

    if found:
        route = [goal]
        while route[-1] != start:
            route.append(cache[route[-1]][1])
        rounded = getcontext().flags[Rounded]
        inexact = getcontext().flags[Inexact]
        return found_cost, route, rounded, inexact

class Node:
    def __init__(self, x, y, left=None, right=None):
        self.x = x
        self.y = y
        self.left = left
        self.right = right


if __name__=='__main__':
    from read_files import read_map
    le_map = read_map("Boston_0_512.map")
    diag_cost = Decimal('1.4142135623730950488')
    # 351	359	354	357	3.82842712
    # fringe_search((351, 359), (354, 357), le_map, diag_cost)
    # 405	67	404	64	3.41421356
    # 10	Boston_0_512.map	512	512	6	409	39	388	43.35533905
    fringe_search((6, 409), (39, 388), le_map, diag_cost)
    # 10	Boston_0_512.map	512	512	2	448	21	482	41.87005768
    # 10	Boston_0_512.map	512	512	67	484	33	504	42.28427124