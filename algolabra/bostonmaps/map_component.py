import itertools


def read_map(filename):
    with open(filename) as f:
        lista = f.read().split("\n")
    height = int(lista[1].split(" ")[1])
    width = int(lista[2].split(" ")[1])
    return height, width, lista[4:]

def read_scenarios(filename):
    with open(filename) as f:
        lista = f.read().split("\n")
    lines = [a.split("\t") for a in lista[1:] if a]
    converted = [[int(a[0]), a[1], int(a[2]), int(a[3]), int(a[4]), int(a[5]), int(a[6]), int(a[7]),
                  float(a[8])] for a in lines]
    scenarios = {key: list(group) for key, group in itertools.groupby(converted, lambda x: x[0])}
    return scenarios

height, width, lista = read_map("Boston_0_512.map")
scenarios = read_scenarios("Boston_0_512.map.scen")



