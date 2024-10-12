from math import sqrt
from decimal import Decimal
from algolabra.fringe.doublelinkedlist import Node


def children(node, citymap):
    """
    Gives the valid neighbors of a node on an octile map.

    :param node: parent Node, needs node.x, node.y
    :param citymap: some kind of map
    :return: list of the (x,y,cost) of valid children
    """
    diag_cost = Decimal(sqrt(2))
    masks = [
        (0, 1, Decimal(1)),
        (1, 1, diag_cost),
        (1, 0, Decimal(1)),
        (1, -1, diag_cost),
        (0, -1, Decimal(1)),
        (-1, -1, diag_cost),
        (-1, 0, Decimal(1)),
        (-1, 1, diag_cost),
        (0, 1, Decimal(1))
    ]

    applied = [(mask[0] + node.x, mask[1] + node.y, mask[2]) for mask in masks]
    open_ground = [1 if 0 <= x < len(citymap[0]) and 0 <= y < len(citymap) and citymap[y][x] == '.' else 0 for x, y, z in applied]
    cleared = []
    for i, (x, y, cost) in enumerate(applied[:8]):
        if cost == 1:
            if open_ground[i] == 1:
                cleared.append((x, y, cost))
        elif open_ground[i - 1] and open_ground[i] and open_ground[i + 1]:
            cleared.append((x, y, cost))
    return cleared


if __name__=='__main__':
    map1 = [["#", "#", "#"], ["#", ".", "."], [".", ".", "."]]
    print(children(Node(1,1), map1))
    print(children(Node(1, 0), map1))
    print(children(Node(0, 1), map1))
    print(children(Node(0, 0), map1))
    pass