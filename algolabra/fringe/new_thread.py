from decimal import Decimal, getcontext, Rounded, Inexact
from collections import deque

from algolabra.common_search_utils.children import children
from algolabra.common_search_utils.heuristics import heuristics
from algolabra.common_search_utils.search_thread import SearchThread

class FringeThread(SearchThread):
    """
    Version for FringeTab. Runs in another thread.

    """
    def __init__(self, parent, start, goal, citymap, scene_slots, data_slots, diag_cost):
        """

        :param parent: parent of QThread. needed.
        :param start: start (x,y)
        :param goal: goal (x,y)
        :param citymap: map as list of lists.
        :param scene_slots: QtSlots from MapScene
        :param data_slots: QtSlots from SearchTab
        """
        super().__init__(parent, start, goal, citymap, scene_slots, data_slots, diag_cost)

    def run(self):
        """
        Runs the actual search
        Overrides method from SearchThread and QThread.

        :return:
        """
        self.fringe_search(self.start_node, self.goal_node, self.citymap, self.diag_cost)
        self.finished.emit()

    def fringe_search(self, start: tuple[int, int], goal: tuple[int, int], citymap: list, diag_cost):
        """
        Rescued this from an abandoned thread. Seems to be the fastest solution.

        :param start:
        :param goal:
        :param citymap:
        :param diag_cost:
        :return:
        """
        map_size = len(citymap)
        diff = diag_cost - Decimal(2)

        now = deque([start])
        later = deque()

        flimit = heuristics(*start, *goal, diff)
        found = False
        found_cost = 0
        cache = {start: (None, 0, flimit)}

        while not found:
            fmin = float('inf')

            while not found and now:
                current = now.popleft()

                ############
                self.signals.node_visited.emit(*current)
                ############

                data = cache[current]
                if not data[2]:
                    cache[current] = data = (data[0], data[1], data[1] + heuristics(*current, *goal, diff))

                if data[2] > flimit:
                    fmin = min(data[2], fmin)
                    later.append(current)
                    continue

                if current == goal:
                    found = True
                    found_cost = data[1]
                    self.signals.result_ready.emit()
                    break

                ############
                self.signals.node_expanded.emit(*current)
                ############

                kids = children(*current, citymap, diag_cost, map_size)

                for kid in kids:
                    gchild = kid[2] + data[1]
                    if (kid[0], kid[1]) not in cache or gchild < cache[kid[0], kid[1]][1]:
                        cache[(kid[0], kid[1])] = current, gchild, None
                        now.appendleft((kid[0], kid[1]))
            flimit = fmin
            ############
            flimit_str = str(flimit)
            self.signals.flimit_set.emit(flimit_str)
            ############
            if not later:
                break
            now, later = later, now

        if found:
            route = [goal]
            while route[-1] != start:
                route.append(cache[route[-1]][0])
            rounded = getcontext().flags[Rounded]
            inexact = getcontext().flags[Inexact]
            return found_cost, route, rounded, inexact
