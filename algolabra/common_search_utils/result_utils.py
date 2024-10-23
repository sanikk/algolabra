import time


def get_timers():
    return [time.perf_counter(), time.process_time(), time.thread_time()]

def handle_return_values(ret, timers):
    if len(ret) == 6:
        cost, route, visited, expanded, rounded, inexact = ret
        return [cost, *timers, visited, expanded, rounded, inexact]
    cost, route, rounded, inexact = ret
    return [cost, *timers, rounded, inexact]

def timered(func):
    def inner_f(*args, **kwargs):
        start_times = get_timers()
        ret = func(*args, **kwargs)
        end_times = get_timers()
        timers = [a - b for a,b in zip(end_times, start_times)]
        return handle_return_values(ret, timers)
    return inner_f