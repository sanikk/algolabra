def children_old(node, citymap):
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


def children(node, citymap):
    diag_cost = 2**0.5
    masks = [
        (0, 1, 1),
        (1, 1, diag_cost),
        (1, 0, 1),
        (1, -1, diag_cost),
        (0, -1, 1),
        (-1, -1, diag_cost),
        (-1, 0, 1),
        (-1, 1, diag_cost),
        (0, 1, 1)
    ]
    applied = [(mask[0] + node.x, mask[1] + node.y, mask[2]) for mask in masks]
    returnable = []
    for i, loc in enumerate(applied[:-1]):
        x, y, cost = loc
        if not 0 <= y < len(citymap[0]) or not 0 <= x < len(citymap[0]):
            continue
        if citymap[y][x] != ".":
            continue
        if cost != 1:
            prevx, prevy, prevcost = applied[i - 1]
            if not 0<=prevx < len(citymap[0]) or not 0<=prevy < len(citymap):
                continue
            if citymap[prevy][prevx] != ".":
                continue
            nex = applied[i+1]
            if not 0 <= nex[1] < len(citymap) or not 0 <= nex[0] < len(citymap[0]):
                continue
            if citymap[nex[1]][nex[0]] != ".":
                continue
        returnable.append(loc)
    return returnable


if __name__=='__main__':
    class Node:
        def __init__(self, x=None, y=None, prev=None, next=None):
            self.x = x
            self.y = y

            self.prev = prev
            self.next = next

    # ###
    # #..
    # ...

    le_map = [["#", "#", "#"], ["#", ".", "."], [".", ".", "."]]
    # print(children_with_corner_rule(Node(1, 1), le_map))
    print("*" * 15)
    # print(children_with_corner_rule(Node(2,0), le_map))
    le_map = [["#", ".", "."], [".", ".", "."], [".", ".", "."]]
    # print(children_with_corner_rule(Node(1, 1), le_map))
