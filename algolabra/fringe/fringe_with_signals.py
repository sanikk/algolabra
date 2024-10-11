from PyQt6.QtCore import QObject, pyqtSignal

from algolabra.fringe.doublelinkedlist import Node, DoubleLinkedList
from algolabra.common_search_utils.heuristics import heuristics
from algolabra.common_search_utils.children import children

class FringeSearch(QObject):

    flimit_set = pyqtSignal(float)
    node_visited = pyqtSignal(int, int)
    node_expanded = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()


    def fringe_search(self, start: tuple[int, int], goal: tuple[int, int], citymap: list):
        """
        Implementation for octile maps. No extra data collection or status prints.
        :param start: starting point (x, y)
        :param goal:  goal point (x, y)
        :param citymap:  map
        :return: cost and route if available
        """

        start_node = Node(*start)
        fringe = DoubleLinkedList(node=start_node)
        cache = [[None for a in line] for line in citymap]

        cache[start_node.y][start_node.x] = 0, None
        flimit = heuristics(start_node, *goal)
        ############
        self.flimit_set.emit(flimit)
        ############
        found = False
        found_cost = 0

        while not found and fringe.head:
            fmin = 1000000
            for node in fringe:
                ############
                self.node_visited.emit(node.x, node.y)
                ############
                g, parent = cache[node.y][node.x]
                f = g + heuristics(node, *goal)
                if f > flimit:
                    fmin = min(f, fmin)
                    continue
                if node.x == goal[0] and node.y == goal[1]:
                    print(f"Found route with cost {g}")
                    found = True
                    found_cost = g
                    break

                ############
                self.node_expanded.emit(node.x, node.y)
                ############
                for x, y, cost in children(node, citymap):
                    g_child = g + cost
                    if cache[y][x]:
                        g_cached, parent = cache[y][x]
                        if g_child >= g_cached:
                            continue
                    fringe.add_child(x, y, node)
                    cache[y][x] = g_child, (node.x, node.y)
                fringe.remove_node(node)
            flimit = fmin
            ############
            self.flimit_set.emit(flimit)
            ############
        if found:
            route = [goal]
            while route[-1] != start:
                x,y = route[-1]
                route.append(cache[y][x][1])
            return found_cost, route
