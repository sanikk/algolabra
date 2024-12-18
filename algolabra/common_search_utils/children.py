from decimal import Decimal


def children(node_x,node_y, citymap, diag_cost, map_size, d1=Decimal('1')):
    """
    Gives children of given node (x,y)


    :param node_x: some kind of x
    :param node_y: some kind of y
    :param citymap: map as a list works
    :param diag_cost: 1, 1.414, Decimal work here
    :param map_size: made for square maps so far
    :param d1: cost of straight x or y movement
    """

    masks = [
        ( 0,-1, d1),
        (-1,-1, diag_cost),
        (-1, 0, d1),
        (-1, 1, diag_cost),
        ( 0, 1, d1),
        ( 1, 1, diag_cost),
        ( 1, 0, d1),
        ( 1,-1, diag_cost)
    ]
    returnable = []
    for i, (dx, dy, cost) in enumerate(masks):
        x, y = node_x + dx, node_y + dy
        if not 0 <= x < map_size:
            continue
        if not 0 <= y < map_size:
            continue
        if citymap[y][x] != '.':
            continue
        if cost != d1:
            dx1,dy1 = node_x + masks[i-1][0], node_y + masks[i-1][1]
            if not (0 <= dx1 < map_size and 0 <= dy1 < map_size and citymap[dy1][dx1] == '.'):
                continue
            dx2, dy2 = node_x + masks[(i+1)%8][0], node_y + masks[(i+1)%8][1]
            if not (0 <= dx2 < map_size and 0 <= dy2 < map_size and citymap[dy2][dx2] == '.'):
                continue
        returnable.append((x, y, cost))
    return returnable
