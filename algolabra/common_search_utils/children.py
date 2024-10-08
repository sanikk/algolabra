def children(node, citymap):
    """
    Gives the valid neighbors of a node on an octile map.

    :param node: parent Node, needs node.x, node.y
    :param citymap: some kind of map
    :return: list of the (x,y,cost) of valid children
    """
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
    pass