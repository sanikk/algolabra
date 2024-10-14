from decimal import Decimal
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
    delta_x = node.x - goalx
    delta_y = node.y - goaly
    result =  max(abs(delta_x), abs(delta_y)) + (diag_cost - 1) * min(abs(delta_x), abs(delta_y))
    return result

def heuristics_for_tuples(startx:int, starty: int, goalx: int, goaly: int, diag_cost: Decimal):
    """
    Octile distance function for heuristics. Gives the optimal distance with no obstacles.


    :param startx:
    :param starty:
    :param diag_cost: Decimal of diag cost, Decimal('2').sqrt() works
    """
    delta_x = startx - goalx
    delta_y = starty - goaly
    result =  max(abs(delta_x), abs(delta_y)) + (diag_cost - 1) * min(abs(delta_x), abs(delta_y))
    return result

if __name__=='__main__':
    heuristics_for_tuples(1, 1, 7,7, Decimal('2').sqrt())