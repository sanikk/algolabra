from decimal import Decimal


def read_map(filename) -> list:
    """
    Read movingai-type map file and preprocess it.

    :param filename: object to use as path
    :return: height, width, map as list of lines
    """
    with open(filename) as f:
        lista = f.read().split("\n")
    return [line for line in lista[4:] if line]

def read_scenarios(filename):
    product = {}
    with open(filename) as f:
        lista = f.read().split("\n")
    lines = [a.split("\t") for a in lista[1:] if a]
    map_title = lines[0][1]
    # bucket, map, (start), (goal), ideal_solution
    converted = [[int(a[0]), (int(a[4]), int(a[5])), (int(a[6]), int(a[7])),
                  Decimal(a[8])] for a in lines]
    for i, scenario in enumerate(converted):
        new_item = [i, *scenario]
        if scenario[0] in product:
            product[scenario[0]].append(new_item)
        else:
            product[scenario[0]] = [new_item]

    return map_title, product


if __name__=='__main__':
    pass
    # height, width, lista = read_map("Boston_0_512.map")
    # scenarios = read_scenarios("Boston_0_512.map.scen")



