from decimal import Decimal, getcontext, Rounded, Inexact
from heapq import heappush, heappop

from algolabra.common_search_utils.heuristics import old_heuristics as heuristics
from algolabra.common_search_utils.children import children


def reconstruct_path(start: tuple[int, int], goal: tuple[int, int], came_from: dict):
    """
    Reconstructs path found with A* into a route.

    :param start: start node
    :param goal: goal node
    :param came_from: dict with routing data
    :return: route as a list of nodes
    """
    path = [goal]
    while path[-1] != start:
        path.append(came_from[path[-1]])
    return path


def astar(start: tuple[int, int],goal: tuple[int, int], citymap: list, diag_cost) -> tuple[Decimal, list, bool, bool]:
    """
    Simple A* using stock heapq.
    Currently uses same children and heuristics as Fringe.

    :param start:
    :param goal:
    :param citymap:
    :return:
    """
    # init
    map_size = len(citymap)
    heap = []
    diff = diag_cost - Decimal('1')
    heappush(heap, (heuristics(*start, *goal, diff), start))
    came_from = {start: 0}
    g_scores = {start:0}

    while heap:
        estimate, current = heappop(heap)
        if current == goal:
            final_cost = g_scores[current]
            rounded = getcontext().flags[Rounded]
            inexact = getcontext().flags[Inexact]

            return final_cost, reconstruct_path(start, goal, came_from), rounded, inexact

        for x, y, cost in children(*current, citymap, diag_cost, map_size):
            child = x, y
            tentative_gscore = g_scores[current] + cost
            if tentative_gscore < g_scores.get(child, 10000000):
                came_from[child] = current
                g_scores[child] = tentative_gscore

                fscore = tentative_gscore + heuristics(x, y, *goal, diff)
                heappush(heap, (fscore, child))
