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
    delta_x = Decimal(node.x - goalx)
    delta_y = Decimal(node.y - goaly)
    result =  max(abs(delta_x), abs(delta_y)) + (diag_cost - Decimal(1)) * min(abs(delta_x), abs(delta_y))
    return result

def heuristics_for_tuples(startx:int, starty: int, goalx: int, goaly: int, diag_cost: Decimal):
    """
    Octile distance function for heuristics. Gives the optimal distance with no obstacles.


    :param startx:
    :param starty:
    :param diag_cost: Decimal of diag cost, Decimal('2').sqrt() works
    """
    delta_x = Decimal(startx - goalx)
    delta_y = Decimal(starty - goaly)
    result =  max(abs(delta_x), abs(delta_y)) + (diag_cost - Decimal('1')) * min(abs(delta_x), abs(delta_y))
    return result

if __name__=='__main__':
    heuristics_for_tuples(1, 1, 7,7, Decimal('2').sqrt())