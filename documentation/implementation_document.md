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

Testing needed!

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
