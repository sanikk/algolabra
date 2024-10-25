from decimal import Decimal, getcontext, Rounded, Inexact
from heapq import heappush, heappop

from algolabra.common_search_utils.heuristics import old_heuristics as heuristics
from algolabra.common_search_utils.children import children as children
from algolabra.common_search_utils.search_thread import SearchThread


class AstarThread(SearchThread):
    """
    A QThread using implementation of A* with QtSignals.
    """
    def __init__(self, parent, start, goal, citymap, scene_slots, data_slots, diag_cost):
        """

        :param parent:
        :param start:
        :param goal:
        :param citymap:
        :param scene_slots:
        :param data_slots:
        """
        super().__init__(parent, start, goal, citymap, scene_slots, data_slots, diag_cost)

    def run(self):
        """
        Overrides run method from SearchThread and QThread.
        Runs the actual search. This is run in another thread.

        :return: None
        """
        cost, route, rounded, inexact = self.astar(self.start_node, self.goal_node, self.citymap)
        print(f"{cost=}, {route=}, {rounded=}, {inexact=}")
        self.finished.emit()

    def reconstruct_path(self, start, goal, came_from):
        """
        Reconstructs path returned by astar.

        :param start:
        :param goal:
        :param came_from:
        :return: path [as list of (x,y) coordinates].
        """
        path = [goal]
        while path[-1] != start:
            path.append(came_from[path[-1]])
        return path


    def astar(self, start: tuple[int, int], goal: tuple[int, int], citymap: list) -> tuple[Decimal, list, bool, bool]:
        """
        Simple implementation with heapq.
        Using supplied diag_cost, children, heuristics.

        :param start: (x,y)
        :param goal: (x,y)
        :param citymap: map as list
        :return: cost, path, Rounded, Inexact
        """
        # init
        diff = self.diag_cost - Decimal('1')
        map_size = len(citymap)
        heap = []
        heappush(heap, (heuristics(*start, *goal, diff), start))
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

            for x, y, cost in children(*current, citymap, self.diag_cost, map_size):
                child = x, y
                tentative_gscore = g_scores[current] + cost
                if tentative_gscore < g_scores.get(child, float('inf')):
                    #
                    self.signals.node_visited.emit(x, y)
                    #
                    came_from[child] = current
                    g_scores[child] = tentative_gscore

                    fscore = tentative_gscore + heuristics(x, y, *goal, diff)
                    heappush(heap, (fscore, child))
