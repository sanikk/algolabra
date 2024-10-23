from decimal import Decimal, getcontext, Inexact, Rounded

from algolabra.common_search_utils.search_thread import SearchThread
from algolabra.fringe.doublelinkedlist import Node, DoubleLinkedList
from algolabra.common_search_utils.heuristics import heuristics_with_node
from algolabra.common_search_utils.children import children_with_node, children


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
        Implementation for octile maps.

        Sends signals of visits, expansions, flimit changes.

        :param start: starting point (x, y)
        :param goal:  goal point (x, y)
        :param citymap:  map
        :param diag_cost: cost of diagonal movement
        :return: cost and route if available
        """
        fmax = 10000000
        start_node = Node(*start, None, None)
        fringe = DoubleLinkedList(node=start_node)
        cache = [[None for a in line] for line in citymap]

        cache[start_node.y][start_node.x] = 0, None
        flimit = heuristics_with_node(start_node, *goal, diag_cost)
        ############
        flimit_str = str(flimit)
        self.signals.flimit_set.emit(flimit_str)
        visited = 0
        expanded = 0
        ############
        found = False
        found_cost = 0

        while not found and fringe.head:
            fmin = fmax
            for node in fringe:
                ############
                self.signals.node_visited.emit(node.x, node.y)
                visited += 1
                ############
                g, parent = cache[node.y][node.x]
                f = g + heuristics_with_node(node, *goal, diag_cost)
                if f > flimit:
                    fmin = min(f, fmin)
                    continue

                if node.x == goal[0] and node.y == goal[1]:
                    print(f"Rounded: {getcontext().flags[Rounded]}, Inexact: {getcontext().flags[Inexact]}")
                    print(f"Found route with cost {g}")
                    print(f"{visited=}, {expanded=}")
                    self.signals.result_ready.emit()
                    found = True
                    found_cost = g
                    break

                ############
                self.signals.node_expanded.emit(node.x, node.y)
                expanded += 1
                ############
                for x, y, cost in children(node.x, node.y, citymap, diag_cost):
                    g_child = g + cost
                    if cache[y][x]:
                        g_cached, parent = cache[y][x]
                        if g_child >= g_cached:
                            continue
                    fringe.add_child(x, y, node)
                    cache[y][x] = g_child, (node.x, node.y)
                fringe.remove_node(node)
            if not found:
                flimit = fmin
                flimit_str = str(flimit)
                self.signals.flimit_set.emit(flimit_str)
        if found:
            route = [goal]
            while route[-1] != start:
                x,y = route[-1]
                route.append(cache[y][x][1])
            return found_cost, route
