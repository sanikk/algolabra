from algolabra.maps.tiny_graph_from_fringe_pdf import tinygraph
from algolabra.astar.astar import astar
from algolabra.fringe.fringe_search import fringe_search



print("Using graph")
print(f"{tinygraph=}")
#print("Running A*")
#print(astar(1, 14, tinygraph))
print("Running Fringe search")
# print(fringe_search(1, 14, tinygraph))
print(fringe_search(1, 14, tinygraph, preset_flimit=3))
