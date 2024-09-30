from algolabra.fringe.fringe_search import fringe_search
from algolabra.scenarios.map_component import read_map, read_scenarios

def run_scenarios(scenario_file, map_path, bucket=None):
    map_file, scenario_list = read_scenarios(scenario_file)
    if bucket:
        scenario_list = [a for a in scenario_list if a[0] == bucket]

    citymap = read_map(map_path or map_file)

    for bucket, start, goal, ideal_solution in scenario_list:
        fringe_search(start, goal, citymap)
        print(f"{ideal_solution=}")
        input()

# bucket, map, mapx, mapy, start_x, start_y, goal_x, goal_y, shortest

if __name__=='__main__':
    run_scenarios("algolabra/bostonmaps/Boston_0_512.map.scen", 0)
