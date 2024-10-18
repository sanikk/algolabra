def handle_path(path: list) -> tuple[int, int, int]:
    """
    Transforms a path into number of straight moves, and number of diagonal moves.
    """
    straight = 0
    diag = 0
    edellinen = None
    for i, piste in enumerate(path):
        if edellinen:
            x_delta = piste[0] - edellinen[0]
            y_delta = piste[1] - edellinen[1]
            if x_delta and y_delta:
                diag += 1
            else:
                straight += 1
        edellinen = piste
    steps = len(path)
    return steps, straight, diag