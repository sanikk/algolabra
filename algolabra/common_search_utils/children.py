from decimal import Decimal


def children(node_x,node_y, citymap, diag_cost, map_size):
    d1 = Decimal(1)

    masks = [
        ( 0,-1, d1),    # N
        (-1,-1, diag_cost),    # NW
        (-1, 0, d1),    # W
        (-1, 1, diag_cost),    # SW
        ( 0, 1, d1),    # S
        ( 1, 1, diag_cost),    # SE
        ( 1, 0, d1),    # E
        ( 1,-1, diag_cost)    # NE
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
            dx,dy = node_x + masks[i-1][0], node_y + masks[i-1][1]
            if not (0 <= dx < map_size and 0 <= dy < map_size and citymap[dy][dx] == '.'):
                continue
            dx, dy = node_x + masks[(i+1)%8][0], node_y + masks[(i+1)%8][1]
            if not (0 <= dx < map_size and 0 <= dy < map_size and citymap[dy][dx] == '.'):
                continue
        returnable.append((x, y, cost))
    return returnable
