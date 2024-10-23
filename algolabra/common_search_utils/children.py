from decimal import Decimal


def children_return_tuple(node, citymap, diag_cost):
    """
    Gives the valid neighbors of a node on an octile map.

    :param node: parent Node, needs node.x, node.y
    :param citymap: some kind of map
    :return: list of the (x,y,cost) of valid children

    Uses x: int, y: int, cost: Decimal internally.
    """
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

    applied = [((mask[0] + node[0], mask[1] + node[1]), mask[2]) for mask in masks]
    open_ground = [1 if 0 <= x < len(citymap[0]) and 0 <= y < len(citymap) and citymap[y][x] == '.' else 0 for (x, y), z in applied]

    cleared = [a for i,a in enumerate(applied[:8]) if (a[1] == 1 and open_ground[i]) or (open_ground[i] and open_ground[i-1] and open_ground[i+1])]
    return cleared

def children_with_node(node, citymap, diag_cost):
    """
    This is an obsolete wrapper function
    """
    print(f"Obsolete function children.children_with_node called")
    return children(node.x, node.y, citymap, diag_cost)

def children(nx, ny, citymap, diag_cost):
    """
    Gives the valid neighbors of a node on an octile map.

    :param node: parent Node, needs node.x, node.y
    :param citymap: some kind of map
    :return: list of the (x,y,cost) of valid children

    Uses x: int, y: int, cost: Decimal internally.
    """
    # TODO name this to children
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

    applied = [(mask[0] + nx, mask[1] + ny, mask[2]) for mask in masks]
    open_ground = [1 if 0 <= x < len(citymap[0]) and 0 <= y < len(citymap) and citymap[y][x] == '.' else 0 for x, y, z in applied]

    cleared = [a for i,a in enumerate(applied[:8]) if (a[2] == 1 and open_ground[i]) or (open_ground[i] and open_ground[i-1] and open_ground[i+1])]
    return cleared

def children_with_tuple(node: tuple[int, int], citymap, diag_cost):
    """
    Gives the valid neighbors of a node on an octile map.

    :param node: parent Node, needs node.x, node.y
    :param citymap: some kind of map
    :return: list of the (x,y,cost) of valid children

    Uses x: int, y: int, cost: Decimal internally.
    """
    return children(node[0], node[1], citymap, diag_cost)



if __name__=='__main__':
    pass