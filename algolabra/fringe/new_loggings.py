import logging
from decimal import Decimal, getcontext, Rounded, Inexact

# from algolabra.fringe.testbed_dll import Node, DoubleLinkedListAddTail as DoubleLinkedList
from algolabra.fringe.data_structs.doublelinkedlist_version import DoubleLinkedList, Node
# from doublelinkedlist_version import DoubleLinkedList, Node
# from algolabra.fringe.doublelinkedlist import DoubleLinkedList, Node
from algolabra.common_search_utils.heuristics import heuristics
from algolabra.common_search_utils.children import children


def fringe_search_with_logging(start: tuple[int, int], goal: tuple[int, int], citymap: list, bucket, scenario, diag_cost):
    logging.basicConfig(filename='fringe.log', level=logging.DEBUG,
                        format='%(message)s')

    fmax = float('inf')
    map_size = len(citymap)

    start_node = Node(*start, None, None)
    fringe = DoubleLinkedList(start_node)

    cache = {start: (0, None)}
    flimit = heuristics(*start, *goal, diag_cost)
    ############
    logging.info(f"Running Fringe for scenario {bucket}{scenario}")
    logging.info(f"starting with flimit {flimit}")
    ############
    found = False
    found_cost = 0
    visited = 0
    expanded = 0
    visits = {}
    expansions = {}

    while not found and fringe:
        fmin = fmax
        # node is a node here
        for node in fringe:
            tup = (node.x, node.y)
            ######
            visited += 1
            if (node.x, node.y) not in visits:
                visits[(node.x, node.y)] = 0
            visits[(node.x, node.y)] += 1
            ######
            g, parent = cache[tup]
            f = g + heuristics(node.x, node.y, *goal, diag_cost)
            if f > flimit:
                logging.info(f"visit {node}({visits[(node.x, node.y)]}): f:{f} over flimit {flimit}")
                fmin = min(f, fmin)
                continue
            if node.x == goal[0] and node.y == goal[1]:
                found = True
                found_cost = g
                print(f"found {g}")
                logging.info(f"visit {node}({visits[(node.x, node.y)]}): found goal with cost {g}")
                break
            ############
            expanded += 1
            if (node.x, node.y) not in expansions:
                expansions[(node.x, node.y)] = 0
            expansions[(node.x, node.y)] += 1
            logging.info(f"visit({visits[(node.x, node.y)]}) - expand({expansions[(node.x, node.y)]}) {node}: ")
            ############
            for x, y, cost in reversed(children(node.x, node.y, citymap, diag_cost, map_size)):
                child = (x, y)
                g_child = g + cost
                if child in cache:
                    g_cached, parent = cache[child]
                    if g_child >= g_cached:
                        logging.info(f"    child {x},{y}: previous {g_cached} was better than this {g_child}")
                        continue
                fringe.add_tail(x, y)
                logging.info(f"    child {x},{y}: adding to F")
                cache[child] = g_child, tup
            fringe.remove_node(node)
            logging.info(f"remove {node} from fringe")
            logging.info(f"fringe: {len(list(fringe))}")
        if not found:
            flimit = fmin
            logging.info(f"setting flimit {flimit}")
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
    fringe_search_with_logging((351, 359), (354, 357), le_map, 0,2, diag_cost)
    # 405	67	404	64	3.41421356