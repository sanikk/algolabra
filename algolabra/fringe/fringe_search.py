def fringe_search(start: int, goal: int, children:list):
    fringe = [start]
    cache = [None for i in children]
    cache[start] = (0, None)
    flimit = heuristics(start, goal)
    print(f"initial {flimit=}")
    found = False

    node_count = 0
    nodes_visited = 0
    nodes_expanded = 0

    while not found and fringe:
        # for state:
        times_visited = 0
        turn_visited = []
        times_expanded = 0
        turn_expanded = []
        fmin = 1000000
        for node in fringe:
            node_count += 1
            times_visited += 1
            turn_visited.append(node)
            g, parent = cache[node]
            f = g + heuristics(node, goal)
            if f > flimit:
                nodes_visited += 1
                fmin = min(f, fmin)
                continue
            if node == goal:
                print(f"found route with cost {g}")
                print(f"{node_count=}, {nodes_visited=}, {nodes_expanded=}")
                # TODO gives out a faulty value.
                found = True
                break

            # käsitellään lapset joten expanded
            nodes_expanded += 1
            times_expanded += 1
            turn_expanded.append(node)

            for child, cost in children[node]:
                nodes_visited += 1
                times_visited += 1
                turn_visited.append(child)
                g_child = g + cost
                if cache[child]:
                    g_cached, parent = cache[child]
                    if g_child >= g_cached:
                        # nodes_visited += 1
                        continue
                if child in fringe:
                    fringe.remove(child)
                fringe.append(child)
                cache[child] = (g_child, node)
            fringe.remove(node)
        flimit = fmin
        print(f"{flimit=}")
        print(f"{times_visited=}, {turn_visited=}")
        print(f"{times_expanded=}, {turn_expanded=}")
        print(f"{fringe=}")
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
