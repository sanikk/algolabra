import time
from decimal import Decimal
from heapq import heappush, heappop
from algolabra.common_search_utils.heuristics import heuristics_for_tuples as heuristics
from algolabra.common_search_utils.children import children_with_tuples as children

def reconstruct_path(start, goal, came_from):
    path = [goal]
    while path[-1] != start:
        path.append(came_from[path[-1]])
    return path

def timed_astar_search(start, goal, citymap):
    start_times = [time.perf_counter(), time.process_time(), time.thread_time()]
    cost, route = astar(start, goal, citymap)
    end_times = [time.perf_counter(), time.process_time(), time.thread_time()]
    timers = [a - b for a, b in zip(end_times, start_times)]

    return cost, timers, route

def astar(start,goal, citymap):
    # init
    diag_cost = Decimal('2').sqrt()
    heap = []
    heappush(heap, (heuristics(*start, *goal, diag_cost), start))
    came_from = {start: 0}
    g_scores = {start:0}

    while heap:
        estimate, current = heappop(heap)
        if current == goal:
            final_cost = g_scores[current]
            # print(f"found! cost {final_cost}")
            return final_cost, reconstruct_path(start, goal, came_from)

        for x, y, cost in children(*current, citymap, diag_cost):
            child = x, y
            tentative_gscore = g_scores[current] + cost
            if tentative_gscore < g_scores.get(child, 10000000):
                came_from[child] = current
                g_scores[child] = tentative_gscore

                fscore = tentative_gscore + heuristics(x, y, *goal, diag_cost)
                heappush(heap, (fscore, child))

if __name__=='__main__':
    pass