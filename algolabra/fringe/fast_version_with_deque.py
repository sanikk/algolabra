from decimal import Decimal, getcontext, Rounded, Inexact
from collections import deque

from algolabra.common_search_utils.children import children
from algolabra.common_search_utils.heuristics import old_heuristics as heuristics


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
    diff = diag_cost - Decimal(1)

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
                print(f"found {data[1]}")
                break

            kids = children(*current, citymap, diag_cost, map_size)

            # due to children insertion order we reverse if going x->0, y -> max

            # hmm. four directions? split and paste to end to rotate? should be fast with only max 8.

            # if  start[0] < goal[0]:
            #     kids.reverse()

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