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
    return old_heuristics(node.x, node.y, goalx, goaly, diff)

def old_heuristics(nx:int, ny: int, goalx: int, goaly: int, diff) -> Decimal:
    """
    Octile distance function for heuristics. Gives the optimal distance with no obstacles.

    :param nx: int x of node
    :param ny: int y of node
    :param goalx: int x of goal
    :param goaly: int y of goal


    function heuristic(node) =
        dx = abs(node.x - goal.x)
        dy = abs(node.y - goal.y)
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
    from http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#diagonal-distance

    if delta_x > delta_y:
        min, max = delta_y, delta_x
    """
    abs_delta_x = abs(nx - goalx)
    abs_delta_y = abs(ny - goaly)

    return max(abs_delta_x, abs_delta_y) + diff * min(abs_delta_x, abs_delta_y)


def new_heuristic(nx, ny, gx, gy, other_diff):
    abs_dx = abs(nx - gx)
    abs_dy = abs(ny - gy)
    return abs_dx + abs_dy + other_diff * min(abs_dx, abs_dy)