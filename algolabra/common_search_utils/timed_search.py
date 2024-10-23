import time


def timed_search(search, start, goal, citymap) -> tuple[int, list, list]:
    """
    Runner for timed fringe search.
    We setup things here for timing.

    uses time.perf_counter for timing
    + process & thread times

    :param search: callable search function that takes (start, goal, citymap) as parameters.
    :param start: (x, y) of start
    :param goal: (x, y) of goal
    :param citymap: a map as container of containers. quack quack.
    :return: cost, timer diffs, route
    """

    start_times = [time.perf_counter(), time.process_time(), time.thread_time()]
    cost, route = search(start, goal, citymap)
    end_times = [time.perf_counter(), time.process_time(), time.thread_time()]
    timers = [a - b for a,b in zip(end_times, start_times)]

    return cost, timers, route

def get_timers():
    return [time.perf_counter(), time.process_time(), time.thread_time()]