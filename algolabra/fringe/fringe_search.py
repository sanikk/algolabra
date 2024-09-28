from codecs import xmlcharrefreplace_errors

from fringe.doublelinkedlist import DoubleLinkedList

# [0, 'Boston_0_512.map', 512, 512, 344, 85, 343, 85, 1.0]
def children(node):
    return [(0,0),(1,1),(2,2),(3,3)]

def fringe_search(start, goal, citymap):
    goaly, goalx = goal
    fringe = DoubleLinkedList(*start)
    cache = [[None for a in line] for line in citymap]
    # cache = [None for i in range(len(map)*)]
    cache[start[0]][start[1]] = (0, None, None)
    flimit = heuristics(start, goal)
    found = False

    while not found and fringe.head:
        fmin = 1000000
        for node in fringe:
            g, parent = cache[node.y][node.x]
            f = g + heuristics(node, goal)
            if f > flimit:
                fmin = min(f, fmin)
                continue
            if node.x == goal.x and node.y == goal.y:
                print(f"found route with cost {g}")
                found = True
                break

            for childy, childx, cost in reversed(children(node)):
                g_child = g + cost
                if cache[childy][childx]:
                    g_cached, parent = cache[childy][childx]
                    if g_child >= g_cached:
                        continue
                # TODO replace this with a doublelinkedlist function. do a search, rm if found.
                # if child in fringe:
                #     fringe.remove_data(child)
                fringe.removal_version(childx, childy)
                fringe.add_node(childx, childy, node=node)
                cache[childy][childx] = (g_child, node.data)
                if childx == goalx and childy == goaly:
                    print(f"{childx=},{childy=}: {g_child=}, {node.data=}")
                    print(f"fringe: {[(node.x,node.y) for node in fringe]}")
            fringe.remove_node(node)

        flimit = fmin
    if found:
        route = [goal]
        while route[-1] != start:
            indeksi = route[-1]
            route.append(cache[indeksi])
        print(route)
        return route


def heuristics(node, goal):
    if node == goal:
        return 0
    # distance * something ideal
    # ohkay this needs small values.
    # that mabbe grow the closer you get?
    # let's do a random value for starters, 1 is random enough :D
    return 1
