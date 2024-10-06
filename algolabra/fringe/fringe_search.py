from algolabra.fringe.doublelinkedlist import DoubleLinkedList, Node
from algolabra.common_search_utils.heuristics import heuristics


def fringe_search(start, goal, citymap):
    """
    Implementation for octile maps.
    Lightly printing to give some data.

    :param start:
    :param goal:
    :param citymap:
    :return:
    """
    start_node = Node(*start)
    fringe = DoubleLinkedList(node=start_node)
    cache = [[None for a in line] for line in citymap]

    cache[start_node.y][start_node.x] = 0, None
    flimit = heuristics(start_node, *goal)
    found = False
    found_cost = 0

    while not found and fringe.head:
        fmin = 1000000
        for node in fringe:
            g, parent = cache[node.y][node.x]
            f = g + heuristics(node, *goal)
            if f > flimit:
                fmin = min(f, fmin)
                continue
            if node.x == goal[0] and node.y == goal[1]:
                found = True
                found_cost = g
                break

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
    if found:
        route = [goal]
        while route[-1] != start:
            x,y = route[-1]
            route.append(cache[y][x][1])
        return found_cost, route

def children(node, citymap):
    """
    Gives the valid neighbors of node in map.
    No reordering yet.

    :param node: Node
    :param citymap: list[y][x]
    :return: [(x,y),(x,y),...]
    """

    diag_cost = 2**0.5
    masks = [(-1, -1, diag_cost), (-1, 0, 1), (-1, 1, diag_cost), (0, -1, 1), (0, 1, 1), (1, -1, diag_cost), (1, 0, 1), (1, 1, diag_cost)]
    applied = [(mask[0] + node.x, mask[1] + node.y, mask[2]) for mask in masks]

    in_area = [child for child in applied if
               0 <= child[1] < len(citymap) and
               0 <= child[0] < len(citymap[0])]
    open_spaces = [loc for loc in in_area if citymap[loc[1]][loc[0]] == "." or "G"]

    return open_spaces[::-1]

def collect_data_fringe_search(start, goal, citymap):
    """
    Implementation for octile maps.
    Lightly printing to give some data.

    :param start:
    :param goal:
    :param citymap:
    :return:
    """
    print(f"{start=}")
    print(f"{goal=}")

    # let's make nodes
    start_node = Node(*start)

    # fringe = DoubleLinkedList(node=start_node)
    fringe = DoubleLinkedList(node=start_node)
    cache = [[None for a in line] for line in citymap]

    cache[start_node.y][start_node.x] = 0, None
    flimit = heuristics(start_node, *goal)
    found = False

    print(f"initial {flimit=}")
    visited = 0
    vlist = []
    expanded = 0
    elist = []

    while not found and fringe.head:
        fmin = 1000000
        for node in fringe:
            # counter stuff
            visited += 1
            vlist.append(node)
            #
            g, parent = cache[node.y][node.x]
            f = g + heuristics(node, *goal)
            # print(f"handling {node=}, {g=}, {parent=}, {f=}")
            if f > flimit:
                fmin = min(f, fmin)
                continue
            if node.x == goal[0] and node.y == goal[1]:
                print(f"found route with cost {g}")
                print(f"{visited=}, {expanded=}")
                # print(f"{g=}, {node.x=}, {node.y=}")
                # print(f"fringe: {[(node.x, node.y) for node in fringe]}")
                found = True
                break

            # counter stuff
            expanded += 1
            elist.append((node.x, node.y))

            for x, y, cost in children(node, citymap):
                # print(f"handling child {x=},{y=}, {cost=}")
                g_child = g + cost
                if cache[y][x]:
                    g_cached, parent = cache[y][x]
                    if g_child >= g_cached:
                        continue
                fringe.add_child(x, y, node)
                cache[y][x] = g_child, (node.x, node.y)
            fringe.remove_node(node)
        # TODO remove this, it just bugged me
        if not found:
            flimit = fmin
            print(f"finished round. updated {flimit=}")
            print(f"{visited=}, {expanded=}")
    if found:
        route = [goal]
        while route[-1] != start:
            x,y = route[-1]
            route.append(cache[y][x][1])
        print(route)
        return route



if __name__=='__main__':
    node = Node(x=1, y=1)
