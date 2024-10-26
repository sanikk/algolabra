from decimal import Decimal


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


def heuristics(nx, ny, gx, gy, other_diff):
    """
    function heuristic(node) =
        dx = abs(node.x - goal.x)
        dy = abs(node.y - goal.y)
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

    where D = 1, D2 = sqrt(2) => diff = diag_cost - 2
    from http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#diagonal-distance

    :param nx: node x
    :param ny: node y
    :param gx: goal x
    :param gy: goal y
    :param other_diff: our replacement of sqrt(2) - 2, with these movement costs
    :return: very good estimate
    """
    abs_dx = abs(nx - gx)
    abs_dy = abs(ny - gy)
    return abs_dx + abs_dy + other_diff * min(abs_dx, abs_dy)
