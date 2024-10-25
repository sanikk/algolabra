# Implementation document

## Project structure

Started with the algorithms so not much yet.
- doublelinkedlist with builtin dict for fringe search
- heuristics function for grid, should be usable in both
- went with qt6 front, since it looks neat

## Achieved space and time complexities

With non-consistent heuristics some nodes will be expanded multiple times. Octile distance is
used as heuristic.

## Performance and O-analysis comparisons

There were small deviations from the ideal solutions, so i [checked](../algolabra/common_search_utils/check_movingai_ideal_solutions.py).
The ideal solutions i checked used either 9 or 10 decimal approximations of sqrt(2). So there will
be slight deviations from the ideal solutions of [movingai](https://www.movingai.com/benchmarks/index.html).

Implementation with python standard modules proved somewhat problematic. As the map
and paths grow the fringe grows as well. 

There are fast solutions using deques, but as the map, path length and fringe size grow
these require more and more upkeep. The DoubleLinkedList version using dict for node tracking loses a bit in speed but the upkeep does
not seem to grow as fast on a larger path or longer maps.

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

ChatGPT is assisting me to consider possible grids faster. Elevation map of Helsinki to
avoid going up/downhill while cycling was considered, to give an example. No coding assistants, I
am still working on search logic which will need troubleshooting so it must be very human-readable.

I abandoned my idea of a Helsinki grid so all LLM assisted data was left unused. LLM was good
for navigating a foreign api.

## References

- fringe pdf 
- a* wiki page
- amit's excellent pages http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
