def read_map(filename) -> tuple[int, int, list]:
    """
    Read movingai-type map file and preprocess it.

    :param filename: object to use as path
    :return: height, width, map as list of lines
    """
    with open(filename) as f:
        lista = f.read().split("\n")
    height = int(lista[1].split(" ")[1])
    width = int(lista[2].split(" ")[1])
    return height, width, [line for line in lista[4:] if line]

def read_scenarios(filename) -> tuple[str, list]:
    """
    Read movingai-type map scenario file and preprocess it.

    :param filename: path to scenario file
    :return: map_title and list of scenarios: [bucket, (start), (goal), ideal_solution]
    """
    with open(filename) as f:
        lista = f.read().split("\n")
    lines = [a.split("\t") for a in lista[1:] if a]
    map_title = lines[0][1]

    # bucket, map, (start), (goal), ideal_solution
    converted = [[int(a[0]), (int(a[4]), int(a[5])), (int(a[6]), int(a[7])),
                  float(a[8])] for a in lines]
    return map_title, converted


if __name__=='__main__':
    pass
    # height, width, lista = read_map("Boston_0_512.map")
    # scenarios = read_scenarios("Boston_0_512.map.scen")



