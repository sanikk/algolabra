from decimal import Decimal
from algolabra.fringe.doublelinkedlist import Node


def heuristics_with_node(node: Node, goalx: int, goaly: int, diff, diag_cost: Decimal) -> Decimal:
    """
    This is an obsolete Wrapper function.

    :param node: Node we calculate a value for
    :param goalx: x coordinate of goal
    :param goaly: y coordinate of goal
    :param diag_cost: cost to move diagonally
    :return: estimate in Decimal
    """
    return heuristics(node.x, node.y, goalx, goaly, diff, diag_cost)

def heuristics(startx:int, starty: int, goalx: int, goaly: int, diff, diag_cost: Decimal) -> Decimal:
    """
    Octile distance function for heuristics. Gives the optimal distance with no obstacles.

    :param startx: int
    :param starty: int
    :param goalx: int
    :param goaly: int
    :param diag_cost: Decimal of diag cost, Decimal('2').sqrt() works
    """
    abs_delta_x = abs(startx - goalx)
    abs_delta_y = abs(starty - goaly)
    # result =  max(abs_delta_x, abs_delta_y) + (diag_cost - 1) * min(abs_delta_x, abs_delta_y)
    result = max(abs_delta_x, abs_delta_y) + (diff) * min(abs_delta_x, abs_delta_y)
    return result
