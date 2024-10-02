from algolabra.maps.tiny_graph_from_fringe_pdf import tinygraph
# from algolabra.astar.astar import astar
from algolabra.fringe.fringe_search import fringe_search
# from algolabra.bostonmaps.map_component import read_map
from algolabra.scenarios.scenarios import read_map, run_scenarios


# [0, 'Boston_0_512.map', 512, 512, 344, 85, 343, 85, 1.0]
# bm = read_map("algolabra/bostonmaps/Boston_0_512.map")
# bm = [line for line in bm if line]
# print("Using graph")
# print(f"{tinygraph=}")
# print("Running A*")
# print(astar(1, 14, tinygraph))

# print("Running Fringe search")
# print(fringe_search(1, 14, tinygraph, preset_flimit=3))
# print(fringe_search((344,85), (343, 85), bm))

# 0	Boston_0_512.map	512	512	121	317	120	320	3.41421356
# print("*"*30)
# print(fringe_search((121, 317), (120, 320), bm))
run_scenarios("algolabra/bostonmaps/Boston_0_512.map.scen", "algolabra/bostonmaps/Boston_0_512.map", 20)