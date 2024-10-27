# Implementation document

## Project structure

Started with the algorithms so not much yet.
- doublelinkedlist with builtin dict for fringe search (too slow, there is a version in the final product. the speeds
didnt go up that much after, so that version should give the picture, if so inclined)
- had to go with deque version. I had the first version finished AFTER the peer review, so I tried to avoid this. There
seems to be nothing in the standard modules that would be better, right now. Let's hope python devs give us shiny toys
to play with.
- heuristics function for grid, should be usable in both
- went with qt6 front, since it looks neat

There are basic tools for wiring up a search funtion with logging, visuals, timings.
View is tabbed and new tabs are easy to add.

## Achieved space and time complexities

With non-consistent heuristics some nodes will be expanded multiple times. Octile distance is
used as heuristic.

## Performance and O-analysis comparisons

There were small deviations from the ideal solutions, so i [checked](../algolabra/common_search_utils/check_movingai_ideal_solutions.py).
The ideal solutions i checked used either 9 or 10 decimal approximations of sqrt(2). So there will
be slight deviations from the ideal solutions of [movingai](https://www.movingai.com/benchmarks/index.html).

---

Implementation with python standard modules proved somewhat problematic. As the map
and paths grow the fringe grows as well. The solutions to this are usually multiple lists, especially on larger maps.

There are fast solutions using deques, but as the map, path length and fringe size grow
these require more and more upkeep and bucket list managing. The deque in python is implemented
as a doublelinked list of lists [(source)](https://github.com/python/cpython/blob/main/Modules/_collectionsmodule.c#L81-L94).
Replicating the speed of this structure within python is currently impossible.

OrderedDict would have hashes, movetoend, and it's also a doublelinked list underneath. Currently there
is no easy way to access the links.
---

Update: Ok I think I got it now. I try this out.

---

Initially there were some "drifts", flimits kept being spread out with 0.0000000000001 differences, which
required either passing through the fringe multiple times, or doing a good enough approximation with the limit. 

There are no practical reasons for the kind of precision used here that I can think of, but just in case we
our future nano-scale robot overlords build even smaller overlords, this might help them navigate.
Also the drift seems to be eliminatable at almost any scale.

## Possible shortcomings and suggestions for improvement

~~Heuristics seem awful at the moment, I need to look into this.~~

Octile distance should give the distance between two points on a grid if there are no obstructions. 
Seems to work so far.

## Usage of LLMs

In places where pytest or Qt documentation is a bit...lacking, the latest ChatGPT was excellent at cooking up
simple examples of accessing an interface. Also used extensively when I was making a grid map of Helsinki in
the first week. I ended up using movingai grid maps.


## References

- fringe pdf 
- a* wiki page
- amit's excellent pages http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
- https://wiki.python.org/moin/TimeComplexity gives some hints when picking data structs