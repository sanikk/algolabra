from maps.tiny_graph_from_fringe_pdf import tinygraph
from astar.astar import astar
from fringe.fringe_search import fringe_search


print(f"{tinygraph=}")
print(astar(1, 14, tinygraph))
print(fringe_search(1, 14, tinygraph))