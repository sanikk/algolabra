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
- the ordered dict version can match A* on larger maps.

There are basic tools for wiring up a search funtion with logging, visuals, timings.
View is tabbed and new tabs are easy to add.

## Achieved space and time complexities

Octile distance is used as heuristic.

There are no huge inefficiencies in either.

## Performance and O-analysis comparisons

There were small deviations from the ideal solutions, so i [checked](../algolabra/common_search_utils/check_movingai_ideal_solutions.py).
The ideal solutions i checked used either 9 or 10 decimal approximations of sqrt(2). So there will
be slight deviations from the ideal solutions of [movingai](https://www.movingai.com/benchmarks/index.html).

---

Implementation with python standard modules proved somewhat problematic. 

There are fast solutions using deques, but as the map, path length and fringe size grow
these require more and more upkeep.

OrderedDict would have hashes, movetoend, and it's also a doublelinked list underneath. Currently there
is no easy way to access the links[(source)](https://github.com/python/cpython/blob/main/Modules/_collectionsmodule.c#L81-L94).
Replicating the speed of this structure within python is currently impossible. OrderedDict would need a different
iterator, one that resolves current.next on \_\_next\_\_, not before, to maintain correct order.

Current best effort, LinkedMap, is built on a dict, not OrderedDict, since maintaining
two linkedlists where the other is not used for anything meaningful is just wasteful. 

---

Initially there were some "drifts", flimits kept being spread out with 0.0000000000001 differences, which
required either passing through the fringe multiple times, or doing a good enough approximation with the limit. 

There are no practical reasons for the kind of precision used here that I can think of, but just in case our 
future nano-scale robot overlords build even smaller over-overlords, this might help them navigate.
Also the drift seems to be eliminatable at almost any scale.

## Possible shortcomings and suggestions for improvement

Octile distance should give the distance between two points on a grid if there are no obstructions. 
Seems to work so far.

Fringe suffers from bad ordering of children nodes due to the order of the masks. It seems there are computationally 
trivial solutions for this.
If the children function works, and the rest of the algorithms work, there seems to
be no real difference in the amount of calls to children between fringe and A*, only a few percent difference there.
If the children function returns wrong nodes fringe will suffer
more from this since there is no reordering of nodes. In A* the reordering from priority queue can 
correct small mistakes. This is an area of this project where it needs improvement.

Fringe seems to call heuristics (or cache if f is there) often 5+ times more than
A*. This causes considerable differences in the load, and requires some care in the
implementation of the heuristics function. I think this version was the best of the 3
to account for the wild variation in the number of calls to heuristics between the
searches. Also caching heuristics results for fringe is a huge speed boost as nodes
start to get revisited.



## Usage of LLMs

In places where pytest or Qt documentation is a bit...lacking, the latest ChatGPT was excellent at cooking up
simple examples of accessing an interface. Also used extensively when I was making a grid map of Helsinki in
the first week. I ended up using movingai grid maps.


## References

- fringe pdf 
- a* wiki page
- amit's excellent pages http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
- https://wiki.python.org/moin/TimeComplexity gives some hints when picking data structs