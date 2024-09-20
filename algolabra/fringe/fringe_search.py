from fringe.doublelinkedlist import DoubleLinkedList


def fringe_search(start: int, goal: int, children:list):
    fringe = DoubleLinkedList(data=start)
    cache = [None for i in children]
    cache[start] = (0, None)
    flimit = heuristics(start, goal)
    found = False

    while not found and fringe.head:
        # for state:
        fmin = 1000000
        for node in fringe:
            g, parent = cache[node.data]
            f = g + heuristics(node.data, goal)
            if f > flimit:
                fmin = min(f, fmin)
                continue
            if node.data == goal:
                print(f"found route with cost {g}")
                found = True
                break

            for child, cost in children[node.data]:
                g_child = g + cost
                if cache[child]:
                    g_cached, parent = cache[child]
                    if g_child >= g_cached:
                        continue
                if child in fringe:
                    # tää pitää ratkasta kohta
                    fringe.remove_data(child)
                fringe.add_data_after_node(data=child, node=node)
                cache[child] = (g_child, node.data)
            fringe.remove_node(node)
        flimit = fmin
    if found:
        route = [goal]
        while route[-1] != start:
            indeksi = route[-1]
            route.append(cache[indeksi][1])
        print(route)
        return route


def heuristics(node, goal):
    # distance * something ideal
    # ohkay this needs small values.
    # that mabbe grow the closer you get?
    # let's do a random value for starters, 1 is random enough :D
    return 1
