# Testing report

    Name                                    Stmts   Miss Branch BrPart  Cover
    -------------------------------------------------------------------------
    algolabra/astar/astar.py                   26     26     10      0     0%
    algolabra/bostonmaps/map_component.py      17     17      8      0     0%
    algolabra/fringe/doublelinkedlist.py       48      2     20      2    94%
    algolabra/fringe/fringe_directed.py        67     67     30      0     0%
    algolabra/fringe/fringe_search.py          63     55     20      1    11%
    -------------------------------------------------------------------------
    TOTAL                                     221    167     88      3    24%

Most of the functions used in Doublelinkedlist so far have been unittested in
the expected scenarios.

Heuristics function has been tested to give right values for 1 square movements, 
this helped me catch an actual bug.

I will later run a few buckets of scenarios on a small map for integration tests.