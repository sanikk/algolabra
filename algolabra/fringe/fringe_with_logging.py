import logging
from decimal import Decimal, getcontext, Rounded, Inexact
from collections import deque

from algolabra.common_search_utils.children import children
from algolabra.common_search_utils.heuristics import heuristics


def fringe_search_with_logging(start: tuple[int, int], goal: tuple[int, int], citymap: list, diag_cost, bucket, scenario, filename=None):
    """
    The deque version with logging.

    :param start:
    :param goal:
    :param citymap:
    :param diag_cost:
    :return:
    """
    ###############
    logging.basicConfig(filename=filename or 'fringe.log', level=logging.DEBUG,
                        format='%(message)s')
    ##############
    map_size = len(citymap)
    diff = diag_cost - Decimal(2)

    now = deque([start])
    later = deque()

    flimit = heuristics(*start, *goal, diff)
    found = False
    found_cost = 0
    cache = {start: (None, 0, flimit)}

    ############
    logging.info(f"Running Fringe for scenario {bucket}{scenario}")
    logging.info(f"starting with flimit {flimit}")
    visited = 0
    visits = {}
    expanded = 0
    expansions = {}
    ############

    while not found:
        fmin = float('inf')

        while not found and now:
            logging.info(f"fringe now: {len(list(now))}")
            current = now.popleft()
            ######
            visited += 1
            if current not in visits:
                visits[current] = 0
            visits[current] += 1
            ######

            data = cache[current]
            if not data[2]:
                cache[current] = data = data[0], data[1], data[1] + heuristics(*current, *goal, diff)

            if data[2] > flimit:
                fmin = min(data[2], fmin)
                later.append(current)
                ###
                logging.info(f"visit {current}({visits[current]}): f:{data[2]} over flimit {flimit}")
                ###
                continue

            if current == goal:
                found = True
                found_cost = data[1]
                ###
                logging.info(f"visit {current}({visits[current]}): found goal with cost {data[1]}")
                ###
                break

            ############
            expanded += 1
            if current not in expansions:
                expansions[current] = 0
            expansions[current] += 1
            logging.info(f"visit({visits[current]}) - expand({expansions[current]}) {current}: ")
            ############

            kids = children(*current, citymap, diag_cost, map_size)

            for kid in kids:
                gchild = kid[2] + data[1]
                if (kid[0], kid[1]) not in cache or gchild < cache[kid[0], kid[1]][1]:
                    cache[(kid[0], kid[1])] = current, gchild, None
                    now.appendleft((kid[0], kid[1]))
                    ###
                    logging.info(f"    child {kid[0]},{kid[1]}: adding to F")
                    ###
                else:
                    ###
                    logging.info(f"    child {kid[0]},{kid[1]}: previous {cache[kid[0], kid[1]][1]} was better than this {gchild}")
                    ###
        flimit = fmin
        ###
        logging.info(f"setting flimit {flimit}")
        ###
        if not later:
            ###
            logging.info(f"path not found. exiting.")
            ###
            break
        now, later = later, now

    if found:
        route = [goal]
        while route[-1] != start:
            route.append(cache[route[-1]][0])
        rounded = getcontext().flags[Rounded]
        inexact = getcontext().flags[Inexact]
        return found_cost, route, rounded, inexact
