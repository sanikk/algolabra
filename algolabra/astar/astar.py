from heapq import heappush, heappop


def reconstruct_path(start, goal, came_from):
    path = [goal]
    while path[-1] != start:
        path.append(came_from[path[-1]])
    return path

def heuristics(current, goal):
    # max_speed = 40 # max speed/min cost
    max_speed = 1  # max speed/min cost
    return (goal-current) * max_speed

def astar(start,goal, children):
    # very basic version with no replace/remove for admissible but not consistent heuristics
    # init
    heap = []
    heappush(heap, (0, start))
    came_from = {start: 0}
    g_scores = {start:0}

    while heap:
        estimate, current = heappop(heap)
        # print(f"{estimate=}, {current=}, {len(heap)=}")
        if current == goal:
            print(f"found! cost {g_scores[current]}")
            return reconstruct_path(1, 14, came_from)

        for child, cost in children[current]:
            # print(f"{cost=}, {child=}")
            tentative_gscore = g_scores[current] + cost
            if tentative_gscore < g_scores.get(child, 10000000):
                came_from[child] = current
                g_scores[child] = tentative_gscore
                fscore = tentative_gscore + heuristics(child, goal)
                heappush(heap, (fscore, child))


