import logging
from decimal import Decimal, getcontext, Rounded, Inexact
from algolabra.fringe.testbed_dll import DoubleLinkedListAddTail as DoubleLinkedList, Node
from algolabra.common_search_utils.heuristics import heuristics
from algolabra.common_search_utils.children import children


def fringe_search_with_logging(start: tuple[int, int], goal: tuple[int, int], citymap: list):
    """
    Implementation for octile maps.

    Logs visits, expansions, handling children.

    :param start: starting point (x, y)
    :param goal:  goal point (x, y)
    :param citymap:  map
    :return: cost and route if available
    """
    logging.basicConfig(filename='fringe.log', level=logging.DEBUG,
                        format='%(relativeCreated)6d %(threadName)s %(message)s')
    diag_cost = Decimal('1.4142135623730950488')
    fmax = 10000000
    start_node = Node(*start, None, None)
    fringe = DoubleLinkedList(node=start_node)
    cache = [[None for a in line] for line in citymap]

    cache[start_node.y][start_node.x] = 0, None
    flimit = heuristics(start_node, *goal, diag_cost)
    ############
    logging.info(f"starting with flimit {flimit}")
    ############
    found = False
    found_cost = 0
    visited = 0
    expanded = 0

    while not found and fringe.head:
        fmin = fmax
        for node in fringe:
            visited += 1
            ############
            g, parent = cache[node.y][node.x]
            f = g + heuristics(node, *goal, diag_cost)
            if f > flimit:
                logging.info(f"visit {node}: f:{f} over flimit {flimit}")
                fmin = min(f, fmin)
                continue
            if node.x == goal[0] and node.y == goal[1]:
                print(f"Found route with cost {g}")
                found = True
                found_cost = g
                logging.info(f"visit {node}: found goal with cost {g}")
                break
            ############
            logging.info(f"visit - expand {node}: ")
            expanded += 1
            ############
            for x, y, cost in children(node, citymap, diag_cost):
                g_child = g + cost
                if cache[y][x]:
                    g_cached, parent = cache[y][x]
                    if g_child >= g_cached:
                        logging.info(f"child {x},{y}: previous {g_cached} was better than this {g_child}")
                        continue
                fringe.add_child(x, y, node)
                cache[y][x] = g_child, (node.x, node.y)
                logging.info(f"child {x},{y}: adding to F")
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
        return found_cost, route, visited, expanded, rounded, inexact

# 09 v:10 e: 3 cost:3.4142

def fringe_search_with_tail_dll(start: tuple[int, int], goal: tuple[int, int], citymap: list):
    """
    Implementation for octile maps.

    Running tests on DoubleLinkedList that just adds to tail since rest of DFS thinking abandoned.

    :param start: starting point (x, y)
    :param goal:  goal point (x, y)
    :param citymap:  map
    :return: cost and route if available
    """
    diag_cost = Decimal('1.4142135623730950488')
    fmax = 10000000

    visited = 0
    expanded = 0

    start_node = Node(*start, None, None)
    # fringe = DLL.__init__(node=start_node)
    fringe = DoubleLinkedList(start_node)
    cache = [[None for a in line] for line in citymap]

    cache[start_node.y][start_node.x] = 0, None
    flimit = heuristics(start_node, *goal, diag_cost)
    found = False
    found_cost = 0

    while not found and fringe.head:
        fmin = fmax
        for node in fringe:
            visited += 1
            g, parent = cache[node.y][node.x]
            f = g + heuristics(node, *goal, diag_cost)
            if f > flimit:
                fmin = min(f, fmin)
                continue
            if node.x == goal[0] and node.y == goal[1]:
                found = True
                found_cost = g
                print(f"found {g}")
                break
            expanded += 1
            for x, y, cost in reversed(children(node, citymap, diag_cost)):
                g_child = g + cost
                if cache[y][x]:
                    g_cached, parent = cache[y][x]
                    if g_child >= g_cached:
                        continue
                # fringe.add_child(x, y, node)
                fringe.add_tail(x, y)
                cache[y][x] = g_child, (node.x, node.y)
            fringe.remove_node(node)
        flimit = fmin
    if found:
        route = [goal]
        while route[-1] != start:
            x,y = route[-1]
            route.append(cache[y][x][1])
        rounded = getcontext().flags[Rounded]
        inexact = getcontext().flags[Inexact]
        return found_cost, route, visited, expanded, rounded, inexact
