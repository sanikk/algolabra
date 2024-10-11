from PyQt6.QtCore import QObject, pyqtSignal, QThread

from algolabra.fringe.doublelinkedlist import Node, DoubleLinkedList
from algolabra.common_search_utils.heuristics import heuristics
from algolabra.common_search_utils.children import children

class FringeSearch(QObject):

    flimit_set = pyqtSignal(float)
    node_visited = pyqtSignal(int, int)
    node_expanded = pyqtSignal(int, int)
    result_ready = pyqtSignal(float)

    def __init__(self, start, goal, citymap, connections):
        super().__init__()
        self.worker_thread = QThread()
        self.start = start
        self.goal = goal
        self.citymap = citymap

    def do_search(self):
        print(f"fringe_with_signals do_search")
        self.fringe_search(self.start, self.goal, self.citymap)


    def fringe_search(self, start: tuple[int, int], goal: tuple[int, int], citymap: list):
        """
        Implementation for octile maps. No extra data collection or status prints.
        :param start: starting point (x, y)
        :param goal:  goal point (x, y)
        :param citymap:  map
        :return: cost and route if available
        """
        print(f"actual search started start:{start}, goal:{goal}")
        start_node = Node(*start)
        fringe = DoubleLinkedList(node=start_node)
        cache = [[None for a in line] for line in citymap]

        cache[start_node.y][start_node.x] = 0, None
        flimit = heuristics(start_node, *goal)
        ############
        self.flimit_set.emit(flimit)
        print(f"initial {flimit=}")
        expanded = 0
        visited = 0
        ############
        found = False
        found_cost = 0

        while not found and fringe.head:
            fmin = 1000000
            for node in fringe:
                ############
                self.node_visited.emit(node.x, node.y)
                visited += 1
                ############
                g, parent = cache[node.y][node.x]
                f = g + heuristics(node, *goal)
                if f > flimit:
                    fmin = min(f, fmin)
                    continue
                if node.x == goal[0] and node.y == goal[1]:
                    print(f"Found route with cost {g}")
                    print(f"{expanded=}, {visited=}")
                    self.result_ready.emit(g)
                    found = True
                    found_cost = g
                    break

                ############
                self.node_expanded.emit(node.x, node.y)
                expanded += 1
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
            flimit = fmin + 0.1
            ############
            self.flimit_set.emit(flimit)
            print(f"{flimit=}, {expanded=}, {visited=}")
            ############
        if found:
            route = [goal]
            while route[-1] != start:
                x,y = route[-1]
                route.append(cache[y][x][1])
            return found_cost, route
