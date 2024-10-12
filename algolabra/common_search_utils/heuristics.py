from decimal import Decimal
from math import sqrt

from algolabra.fringe.doublelinkedlist import Node


def heuristics(node: Node, goalx: int, goaly: int, diag_cost: Decimal):
    """
    Octile distance function for heuristics. Gives the optimal distance with no obstacles.

    :param node: Node we calculate a value for
    :param goalx: x coordinate of goal
    :param goaly: y coordinate of goal
    :param diag_cost: cost to move diagonally
    :return:
    """
    # undirected heuristics and cache for now
    print(f"{type(diag_cost)=}")
    delta_x = Decimal(node.x - goalx)
    print(f"{type(delta_x)=}")
    delta_y = Decimal(node.y - goaly)
    print(f"{type(delta_y)=}")
    result =  max(abs(delta_x), abs(delta_y)) + (diag_cost - Decimal(1)) * min(abs(delta_x), abs(delta_y))
    print(f"{type(result)=}")
    return result
