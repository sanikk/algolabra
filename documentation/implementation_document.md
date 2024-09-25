# Implementation document

## Project structure

Started with the algorithms so not much yet.
- doublelinkedlist for fringe search

## Achieved space and time complexities

With non-consistent heuristics some nodes will be expanded multiple times.

## Performance and O-analysis comparisons

Testing needed!

## Possible shortcomings and suggestions for improvement

The doublelinked list required by the fringe search algorithm needs to know next in line at the time it is popped. This required some modifications.
In the end a mock starter node in the iterator seemed the path of spending least effort and least resources.
Since iterators are single-use components in python the starter node containing next:head gets expended first and there
remain no references to it, so the cost in memory and developer time should be minimal.

## Usage of LLMs

ChatGPT is assisting me to consider possible grids faster. Elevation map of Helsinki to
avoid going up/downhill while cycling was considered, to give an example. No coding assistants, I
am still working on search logic which will need troubleshooting so it must be very human-readable.

## References

- fringe pdf
- a* wiki
