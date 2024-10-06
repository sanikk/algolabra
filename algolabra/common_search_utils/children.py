def children(node, citymap):
    """
    Gives the valid neighbors of node in map.
    No reordering yet.

    :param node: Node
    :param citymap: list[y][x]
    :return: [(x,y),(x,y),...]
    """

    diag_cost = 2**0.5
    masks = [(-1, -1, diag_cost), (-1, 0, 1), (-1, 1, diag_cost), (0, -1, 1), (0, 1, 1), (1, -1, diag_cost), (1, 0, 1), (1, 1, diag_cost)]
    applied = [(mask[0] + node.x, mask[1] + node.y, mask[2]) for mask in masks]

    in_area = [child for child in applied if
               0 <= child[1] < len(citymap) and
               0 <= child[0] < len(citymap[0])]
    open_spaces = [loc for loc in in_area if citymap[loc[1]][loc[0]] == "." or "G"]

    return open_spaces[::-1]
