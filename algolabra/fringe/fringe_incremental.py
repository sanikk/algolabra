from algolabra.fringe.doublelinkedlist import DoubleLinkedList, Node
from algolabra.bostonmaps.map_component import read_map
# from doublelinkedlist import DoubleLinkedList


def fringe_search(start, goal, citymap):
    print(f"{start=}")
    print(f"{goal=}")
    print(f"{len(citymap)=}")
    # let's make nodes
    start_node = Node(*start)
    # TODO remove this, we can use x,y in heuristics
    goal_node = Node(*goal)

    fringe = DoubleLinkedList(node=start_node)
    cache = [[None for a in line] for line in citymap]

    cache[start_node.y][start_node.x] = 0, None
    flimit = heuristics(start_node, goal_node)
    found = False
    print(f"initial {flimit=}")

    while not found and fringe.head:
        fmin = 1000000
        for node in fringe:
            g, parent = cache[node.y][node.x]
            f = g + heuristics(node, goal_node)
            print(f"handling {node=}, {g=}, {parent=}, {f=}")
            if f > flimit:
                fmin = min(f, fmin)
                continue
            if node.x == goal_node.x and node.y == goal_node.y:
                print(f"found route with cost {g}")
                found = True
                break

            for x,y in children(node, citymap):
                print(f"handling child {x=},{y=}")
                g_child = g + 1
                if cache[y][x]:
                    g_cached, parent = cache[y][x]
                    if g_child >= g_cached:
                        continue
                # TODO replace this with a doublelinkedlist function. do a search, rm if found.
                # if child in fringe:
                #     fringe.remove_data(child)
                fringe.removal_version(x, y)
                fringe.add_node(x=x, y=y, node=node)
                cache[y][x] = (g_child, (node.x, node.y))
                if x == goal[0] and y == goal[1]:
                    print(f"found route with cost {g_child}")
                    print(f"{x=},{y=}: {g_child=}, {node.x=}, {node.y=}")
                    print(f"fringe: {[(node.x,node.y) for node in fringe]}")
                    found = True

            fringe.remove_node(node)

        flimit = fmin
        print(f"updated {flimit=}")
    if found:
        print(f"{start=}")
        print(f"{goal=}")
        route = [goal]
        while route[-1] != start:
            print(f"{route=}")
            x,y = route[-1]
            print(f"{route[-1]}")
            print(f"{cache[y][x]=}")
            route.append(cache[y][x][1])
        print(route)
        return route


def heuristics(node, goal):
    # undirected heuristics and cache for now
    if node == goal:
        return 0
    delta_x = node.x - goal.x
    delta_y = node.y - goal.y

    return max(abs(delta_x), abs(delta_y)) + (2**0.5 - 1) * min(delta_x, delta_y)

def children(node, citymap):
    """
    Gives the valid neighbors of node in map.
    :param node: Node
    :param citymap: list[y][x]
    :return: [(x,y),(x,y),...]
    """
    # we could just order the masks in the direction of goal node.
    masks = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    applied = [(mask[0] + node.x, mask[1] + node.y) for mask in masks]
    print(f"children {applied=}")
    in_area = [child for child in applied if
               0 <= child[1] < len(citymap) and
               0 <= child[0] < len(citymap[0])]
    print(f"{in_area=}")
    open_spaces = [loc for loc in in_area if citymap[loc[1]][loc[0]] == "." or "G"]
    # and then reverse the dir here before returning.
    return open_spaces[::-1]