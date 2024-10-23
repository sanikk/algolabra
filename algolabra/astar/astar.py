import time
from decimal import Decimal, getcontext, Rounded, Inexact
from heapq import heappush, heappop

from algolabra.common_search_utils.heuristics import heuristics
from algolabra.common_search_utils.children import children
from algolabra.common_search_utils.timed_search import get_timers


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

def timed_astar_search(start: tuple[int, int], goal: tuple[int, int], citymap: list, diag_cost):
    """
    Times an A* run.
    :param start:
    :param goal:
    :param citymap:
    :return:cost: cost (as Decimal)
            timers: perf, proc and thread time_deltas
            route: path found as an ordered list of nodes.
            rounded: bool if result was rounded, provided by decimal
            inexact: bool if result was inexact, provided by decimal

    """
    start_times = get_timers()

    cost, route, rounded, inexact = astar(start, goal, citymap, diag_cost)

    end_times = get_timers()
    timings = [a - b for a, b in zip(end_times, start_times)]

    return cost, timings, route, rounded, inexact

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
    heap = []
    heappush(heap, (heuristics(*start, *goal, diag_cost), start))
    came_from = {start: 0}
    g_scores = {start:0}

    while heap:
        estimate, current = heappop(heap)
        if current == goal:
            final_cost = g_scores[current]
            rounded = getcontext().flags[Rounded]
            inexact = getcontext().flags[Inexact]

            return final_cost, reconstruct_path(start, goal, came_from), rounded, inexact

        for x, y, cost in children(*current, citymap, diag_cost):
            child = x, y
            tentative_gscore = g_scores[current] + cost
            if tentative_gscore < g_scores.get(child, 10000000):
                came_from[child] = current
                g_scores[child] = tentative_gscore

                fscore = tentative_gscore + heuristics(x, y, *goal, diag_cost)
                heappush(heap, (fscore, child))
