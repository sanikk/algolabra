# from algolabra.fringe.doublelinkedlist import DoubleLinkedList, Node
from doublelinkedlist import DoubleLinkedList, Node


def fringe_search(start, goal, citymap):
    print(f"{start=}")
    print(f"{goal=}")

    # let's make nodes
    start_node = Node(*start)

    fringe = DoubleLinkedList(node=start_node)
    cache = [[None for a in line] for line in citymap]

    cache[start_node.y][start_node.x] = 0, None
    flimit = heuristics(start_node, *goal)
    found = False
    print(f"initial {flimit=}")

    while not found and fringe.head:
        fmin = 1000000
        for node in fringe:
            g, parent = cache[node.y][node.x]
            f = g + heuristics(node, *goal)
            print(f"handling {node=}, {g=}, {parent=}, {f=}")
            if f > flimit:
                fmin = min(f, fmin)
                continue
            if node.x == goal[0] and node.y == goal[1]:
                print(f"found route with cost {g}")
                print(f"{g=}, {node.x=}, {node.y=}")
                print(f"fringe: {[(node.x, node.y) for node in fringe]}")
                found = True
                break

            for x, y, cost in children(node, citymap):
                print(f"handling child {x=},{y=}, {cost=}")
                g_child = g + cost
                if cache[y][x]:
                    g_cached, parent = cache[y][x]
                    if g_child >= g_cached:
                        continue
                # TODO replace this with a doublelinkedlist function. do a search, rm if found.
                # if child in fringe:
                #     fringe.remove_data(child)
                fringe.remove_at_xy(x, y)
                fringe.add_node(x=x, y=y, node=node)
                cache[y][x] = g_child, (node.x, node.y)
            fringe.remove_node(node)

        flimit = fmin
        print(f"updated {flimit=}")
    if found:
        route = [goal]
        while route[-1] != start:
            x,y = route[-1]
            route.append(cache[y][x][1])
        print(route)
        return route


def heuristics(node, goalx, goaly):
    # undirected heuristics and cache for now
    delta_x = node.x - goalx
    delta_y = node.y - goaly
    return max(abs(delta_x), abs(delta_y)) + (2**0.5 - 1) * min(abs(delta_x), abs(delta_y))

def children(node, citymap):
    """
    Gives the valid neighbors of node in map.
    :param node: Node
    :param citymap: list[y][x]
    :return: [(x,y),(x,y),...]
    """
    # we could just order the masks in the direction of goal node.
    diag_cost = 2**0.5
    masks = [(-1, -1, diag_cost), (-1, 0, 1), (-1, 1, diag_cost), (0, -1, 1), (0, 1, 1), (1, -1, diag_cost), (1, 0, 1), (1, 1, diag_cost)]
    applied = [(mask[0] + node.x, mask[1] + node.y, mask[2]) for mask in masks]

    in_area = [child for child in applied if
               0 <= child[1] < len(citymap) and
               0 <= child[0] < len(citymap[0])]
    open_spaces = [loc for loc in in_area if citymap[loc[1]][loc[0]] == "." or "G"]
    # and then reverse the dir here before returning.

    # should run heuristics here and sort the children
    return open_spaces[::-1]

if __name__=='__main__':
    node = Node(x=1, y=1)
    print(f"{node.x=}, {node.y=}")
    print(heuristics(node, 0, 1))
    print(heuristics(node, 0, 0))
    print(heuristics(node, 2, 2))