from decimal import Decimal


def children(nx: int, ny: int, citymap, diag_cost: Decimal, map_size: int):
    """
        Gives the valid neighbors of a node on an octile map.

        :param nx, ny x,y of node
        :param citymap: some kind of map
        :return: list of the (x,y,cost) of valid children

        Uses x: int, y: int, cost: Decimal internally.
        """
    d1 = Decimal(1)
    masks = [
        (0, -1, d1),         # N
        (-1, -1, diag_cost), # NW
        (-1, 0, d1),         # W
        (-1, 1, diag_cost),  # SW
        (0, 1, d1),          # S
        (1, 1, diag_cost),   # SE
        (1, 0, d1),          # E
        (1, -1, diag_cost),  # NE
    ]
    returnable = []
    for i, (dx, dy, cost) in enumerate(masks):
        x,y = nx + dx, ny + dy
        if not 0 <= x < map_size or not 0 <= y < map_size:
            continue
        if citymap[y][x] != '.':
            continue
        if cost!=1:
            px, py = nx + masks[i - 1][1], ny + masks[i - 1][0]
            if not 0 <= px < map_size or not 0 <= py < map_size or not citymap[py][px] == '.':
                continue
            px, py = ny + masks[(i + 1) % 8][1], nx + masks[(i + 1) % 8][0]
            if not 0 <= px < map_size or not 0 <= py < map_size or not citymap[py][px] == '.':
                continue
        returnable.append((x,y,cost))
    return returnable


if __name__=='__main__':
    diag_cost = Decimal('1.4142135623730950488')
    m = [[".", ".", "."], [".", "#", "."], [".", ".", "."]]
    ret = children(1, 0, m, diag_cost, 3)
    print("children from 1,0 with north blocked")
    print(ret)
    m = [[".", "#", "."], [".", ".", "."], [".", ".", "."]]
    ret = children(1, 1, m, diag_cost, 3)
    print("children from 1,1 with north blocked")
    print(ret)