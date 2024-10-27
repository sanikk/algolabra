from decimal import Decimal, getcontext, Rounded, Inexact

from algolabra.fringe.ordered_set_version2 import LastUpdatedOrderedDict, Node
from algolabra.common_search_utils.heuristics import heuristics
from algolabra.common_search_utils.children import children as children


def fringe_search(start: tuple[int, int], goal: tuple[int, int], citymap: list, diag_cost):
    map_size = len(citymap)
    diff = diag_cost - Decimal('2')

    start_node = Node(*start, None, None)
    fringe = LastUpdatedOrderedDict(start, start_node)

    flimit = heuristics(*start, *goal, diff)

    cache = {start: (0, None, flimit)}

    found = False
    found_cost = 0

    while not found and fringe:
        fmin = float('inf')
        # node is a node here
        fringe_iterator = iter(fringe)
        for node in fringe_iterator:
            # print(f"{node=}, x:{node.x}, y:{node.y}")
            g, parent, f = cache[(node.x, node.y)]
            if not f:
                f = g + heuristics(node.x, node.y, *goal, diff)
                cache[(node.x, node.y)] = (g, parent, f)
            if f > flimit:
                fmin = min(f, fmin)
                continue
            if node.x == goal[0] and node.y == goal[1]:
                found = True
                found_cost = g
                print(f"found {g}")
                break
            # time this reverse
            for x, y, cost in reversed(children(node.x, node.y, citymap, diag_cost, map_size)):
                child = (x, y)
                g_child = g + cost
                if child in cache:
                    if g_child >= cache[child][0]:
                        continue
                fringe.add_tail(x,y)
                cache[child] = g_child, (node.x, node.y), None
            fringe.remove_by_node(node)
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
    # fringe_search((351, 359), (354, 357), le_map, diag_cost)
    # 405	67	404	64	3.41421356
    # 10	Boston_0_512.map	512	512	6	409	39	388	43.35533905
    fringe_search((6, 409), (39, 388), le_map, diag_cost)
    # 10	Boston_0_512.map	512	512	2	448	21	482	41.87005768
    # 10	Boston_0_512.map	512	512	67	484	33	504	42.28427124
    #
    #
    # KeyError: (185, 232) scen 367
    # why is the key not there? it should be RIGHT. THERE. !!!. :D
