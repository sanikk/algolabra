import logging
from decimal import getcontext, Rounded, Inexact

from algolabra.fringe.doublelinkedlist import DoubleLinkedList, Node
from algolabra.common_search_utils.heuristics import heuristics_with_node
from algolabra.common_search_utils.children import children


def fringe_search_with_logging(start: tuple[int, int], goal: tuple[int, int], citymap: list, bucket, scenario, diag_cost):
    """
    Implementation for octile maps.

    Logs visits, expansions, handling children

    :param start: starting point (x, y)
    :param goal:  goal point (x, y)
    :param citymap:  map
    :return: cost and route if available
    """
    logging.basicConfig(filename='fringe.log', level=logging.DEBUG,
                        format='%(message)s')

    fmax = float('inf')
    start_node = Node(*start, None, None)
    fringe = DoubleLinkedList(node=start_node)
    cache = [[None for a in line] for line in citymap]

    cache[start_node.y][start_node.x] = 0, None
    flimit = heuristics_with_node(start_node, *goal, diag_cost)
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

    while not found and fringe.head:
        fmin = fmax
        for node in fringe:
            visited += 1
            if (node.x, node.y) not in visits:
                visits[(node.x, node.y)] = 0
            visits[(node.x, node.y)] += 1
            ############
            g, parent = cache[node.y][node.x]
            f = g + heuristics_with_node(node, *goal, diag_cost)
            if f > flimit:
                logging.info(f"visit {node}({visits[(node.x, node.y)]}): f:{f} over flimit {flimit}")
                fmin = min(f, fmin)
                continue
            if node.x == goal[0] and node.y == goal[1]:
                print(f"Found route with cost {g}")
                found = True
                found_cost = g
                logging.info(f"visit {node}({visits[(node.x, node.y)]}): found goal with cost {g}")
                break
            ############
            expanded += 1
            if (node.x, node.y) not in expansions:
                expansions[(node.x, node.y)] = 0
            expansions[(node.x, node.y)] += 1
            logging.info(f"visit({visits[(node.x, node.y)]}) - expand({expansions[(node.x, node.y)]}) {node}: ")
            ############
            for x, y, cost in children(node.x, node.y, citymap, diag_cost):
                g_child = g + cost
                if cache[y][x]:
                    g_cached, parent = cache[y][x]
                    if g_child >= g_cached:
                        logging.info(f"    child {x},{y}: previous {g_cached} was better than this {g_child}")
                        continue
                fringe.add_child(x, y, node)
                cache[y][x] = g_child, (node.x, node.y)
                logging.info(f"    child {x},{y}: adding to F")
            fringe.remove_node(node)
            logging.info(f"remove {node} from fringe")
            logging.info(f"fringe: {list(fringe)}")
        if not found:
            flimit = fmin
            logging.info(f"setting flimit {flimit}")
    if found:
        route = [goal]
        while route[-1] != start:
            x,y = route[-1]
            route.append(cache[y][x][1])
        rounded = getcontext().flags[Rounded]
        inexact = getcontext().flags[Inexact]
        logging.info(f"{rounded=}, {inexact=}")
        logging.info(f"{visited=}, {expanded=}")
        return found_cost, route, visited, expanded, rounded, inexact
