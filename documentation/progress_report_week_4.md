# Week 4
Spent way too much time doing a grid on Helsinki. Most of it is usable but no time to kick up a demo.

Added first map of Boston from https://www.movingai.com/benchmarks/.
Skeletons of functions to read the maps and scenarios.

Adapted fringe search to use the new map. Still missing corners, and heuristics ~~is~~ was giving
some very strange results. (1,1) => (0,0) cost: 1.414....(1,1) => (2,2) cost 0.5858.
Silly bug(tm).

I now want to do two different directed versions of fringe search, if time permits.
