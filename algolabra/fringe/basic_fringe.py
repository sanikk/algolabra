from decimal import Decimal, getcontext, Rounded, Inexact

from algolabra.fringe.dll_clean import DoubleLinkedList, Node
from algolabra.common_search_utils.heuristics import heuristics as heuristics, new_heuristic
from algolabra.common_search_utils.children import children as children
from profilehooks import profile

@profile
def fringe_search(start: tuple[int, int], goal: tuple[int, int], citymap: list, diag_cost):
    fmax = float('inf')
    map_size = len(citymap)
    diff = diag_cost - Decimal('2')

    start_node = Node(*start, None, None)
    fringe = DoubleLinkedList(start_node)


    flimit = new_heuristic(*start, *goal, diff)

    cache = {start: (0, None, flimit)}

    found = False
    found_cost = 0

    while not found and fringe:
        fmin = fmax
        # node is a node here
        for node in fringe:
            g, parent, f = cache[(node.x, node.y)]
            if not f:
                f = g + new_heuristic(node.x, node.y, *goal, diff)
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
                fringe.add_child_to_tail(x,y)
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
    # 13	168	51	134	52.08326111
    fringe_search((13, 168), (51, 134), le_map, diag_cost)