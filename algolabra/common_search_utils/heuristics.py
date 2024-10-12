from decimal import Decimal
from math import sqrt

from algolabra.fringe.doublelinkedlist import Node


def heuristics(node: Node, goalx: int, goaly: int):
    """
    Octile distance function for heuristics. Gives the optimal distance with no obstacles.

    :param node: Node we calculate a value for
    :param goalx: x coordinate of goal
    :param goaly: y coordinate of goal
    :return:
    """
    # undirected heuristics and cache for now
    delta_x = node.x - goalx
    delta_y = node.y - goaly
    return Decimal(max(abs(delta_x), abs(delta_y)) + (Decimal(sqrt(2)) - Decimal(1)) * min(abs(delta_x), abs(delta_y)))
