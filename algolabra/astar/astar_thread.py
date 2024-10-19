from decimal import Decimal, getcontext, Rounded, Inexact
from heapq import heappush, heappop

from algolabra.common_search_utils.heuristics import heuristics_for_tuples as heuristics
from algolabra.common_search_utils.children import children_with_tuples as children
from algolabra.common_search_utils.search_thread import SearchThread
from algolabra.ui.mysignals import FringeSignals

class AstarThread(SearchThread):
    def __init__(self, parent, start, goal, citymap, scene_slots, data_slots):
        super().__init__(parent, start, goal, citymap, FringeSignals(), scene_slots, data_slots)

    def run(self):
        cost, route, rounded, inexact = self.astar(self.start_node, self.goal_node, self.citymap)
        print(f"{cost=}, {route=}, {rounded=}, {inexact=}")
        self.finished.emit()

    def reconstruct_path(self, start, goal, came_from):
        path = [goal]
        while path[-1] != start:
            path.append(came_from[path[-1]])
        return path


    def astar(self, start, goal, citymap):
        # init
        diag_cost = Decimal('1.4142135623730950488')
        heap = []
        heappush(heap, (heuristics(*start, *goal, diag_cost), start))
        #
        self.signals.flimit_set.emit(str(heap[0]))
        #
        came_from = {start: 0}
        g_scores = {start:0}

        while heap:
            estimate, current = heappop(heap)
            #
            self.signals.flimit_set.emit(str(estimate))
            self.signals.node_expanded.emit(*current)
            #
            if current == goal:
                print("FOUND!!")
                final_cost = g_scores[current]
                rounded = getcontext().flags[Rounded]
                inexact = getcontext().flags[Inexact]

                return final_cost, self.reconstruct_path(start, goal, came_from), rounded, inexact

            for x, y, cost in children(*current, citymap, diag_cost):
                child = x, y
                tentative_gscore = g_scores[current] + cost
                if tentative_gscore < g_scores.get(child, 10000000):
                    #
                    self.signals.node_visited.emit(x, y)
                    #
                    came_from[child] = current
                    g_scores[child] = tentative_gscore

                    fscore = tentative_gscore + heuristics(x, y, *goal, diag_cost)
                    heappush(heap, (fscore, child))

if __name__=='__main__':
    pass