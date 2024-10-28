from decimal import Decimal, getcontext, Rounded, Inexact

from algolabra.fringe.linked_dict_for_fringe import LinkedDictForFringe, Linknode

from algolabra.common_search_utils.children import children
from algolabra.common_search_utils.heuristics import heuristics


def fringe_search(start: tuple[int, int], goal: tuple[int, int], citymap: list, diag_cost):
    """
    Ok do not run this. I guess this might be bleeding over a bit?

    Also this way too slow. See LinkedDictForFringe

    :param start:
    :param goal:
    :param citymap:
    :param diag_cost:
    :return:
    """
    map_size = len(citymap)
    diff = diag_cost - Decimal(2)

    ###
    fringe = LinkedDictForFringe((start))
    ###

    flimit = heuristics(*start, *goal, diff)
    found = False
    found_cost = 0
    cache = {start: (None, 0, flimit)}

    while not found:
        fmin = float('inf')

        for current in fringe:
            data = cache[current]
            if not data[2]:
                data = (data[0], data[1], data[1] + heuristics(*current, *goal, diff))
                cache[current] = data

            if data[2] > flimit:
                fmin = min(data[2], fmin)
                continue

            if current == goal:
                # print(f"found with cost {data[1]}")
                found = True
                found_cost = data[1]
                break

            kids = children(*current, citymap, diag_cost, map_size)

            for kid in kids:
                gchild = kid[2] + data[1]
                if kid[:2] not in cache or gchild < cache[kid[:2]][1]:
                    cache[kid[:2]] = current, gchild, None
                    # fringe[kid[:2]] = None
                    fringe.add_tail(kid[:2])
        if not found:
            flimit = fmin

    if found:
        route = [goal]
        while route[-1] != start:
            route.append(cache[route[-1]][0])
        rounded = getcontext().flags[Rounded]
        inexact = getcontext().flags[Inexact]
        return found_cost, route, rounded, inexact
