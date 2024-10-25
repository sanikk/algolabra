from decimal import Decimal, getcontext, Rounded, Inexact

from algolabra.fringe.doublelinkedlist import DoubleLinkedList, Node
from algolabra.common_search_utils.heuristics import heuristics as heuristics
from algolabra.common_search_utils.children import children as children


def fringe_search(start: tuple[int, int], goal: tuple[int, int], citymap: list, diag_cost):
    fmax = float('inf')
    map_size = len(citymap)
    diff = diag_cost - Decimal('1')

    start_node = Node(*start, None, None)
    fringe = DoubleLinkedList(start_node)

    cache = {start: (0, None)}
    flimit = heuristics(*start, *goal, diff, diag_cost)
    found = False
    found_cost = 0

    while not found and fringe:
        fmin = fmax
        # node is a node here
        for node in fringe:
            tup = (node.x, node.y)
            g, parent = cache[tup]
            f = g + heuristics(node.x, node.y, *goal, diff, diag_cost)
            if f > flimit:
                fmin = min(f, fmin)
                continue
            if node.x == goal[0] and node.y == goal[1]:
                found = True
                found_cost = g
                break
            for x, y, cost in reversed(children(node.x, node.y, citymap, diag_cost, map_size)):
                child = (x, y)
                g_child = g + cost
                if child in cache:
                    g_cached, parent = cache[child]
                    if g_child >= g_cached:
                        continue
                fringe.add_tail(x, y)
                cache[child] = g_child, tup
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


if __name__=='__main__':

    from read_files import read_map
    le_map = read_map("Boston_0_512.map")
    diag_cost = Decimal('1.4142135623730950488')
    # 351	359	354	357	3.82842712
    fringe_search((351, 359), (354, 357), le_map, diag_cost)
    # 405	67	404	64	3.41421356