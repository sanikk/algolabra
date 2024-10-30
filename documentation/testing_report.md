# Testing report

    Name                                                              Stmts   Miss Branch BrPart  Cover
    ---------------------------------------------------------------------------------------------------
    algolabra/astar/astar.py                                             31      0     10      0   100%
    algolabra/astar/astar_thread.py                                      47      4     16      0    94%
    algolabra/common_search_utils/check_movingai_ideal_solutions.py      16     16      0      0     0%
    algolabra/common_search_utils/check_solution.py                      14      0      6      0   100%
    algolabra/common_search_utils/children.py                            22      0     14      0   100%
    algolabra/common_search_utils/heuristics.py                           9      0      0      0   100%
    algolabra/common_search_utils/result_utils.py                        17     11      2      0    32%
    algolabra/common_search_utils/search_thread.py                       20     14      0      0    30%
    algolabra/fileIO/read_files.py                                       18     12      8      0    31%
    algolabra/fringe/fringe_thread.py                                    65      5     32      1    94%
    algolabra/fringe/fringe_with_linked_map.py                           43      0     20      1    98%
    algolabra/fringe/fringe_with_logging.py                              69      0     24      1    99%
    algolabra/fringe/fringe_with_two_deques.py                           45      0     20      0   100%
    algolabra/fringe/linked_map.py                                       40      4     16      2    89%
    algolabra/service/scenario_service.py                                59     31     14      1    40%
    algolabra/service/search_service.py                                  65     37     12      0    44%
    ---------------------------------------------------------------------------------------------------
    TOTAL                                                               580    134    194      6    79%

A* and Fringe have been tested to output right costs. The results should be accurate to 10^-18, there is
a test for that.

Most of the focus ended up on the data structures and their testing under load. There is a lot of removals,
lookups, moving to the end happening during a search and the structure must be able to handle that.
There are light unittests to see if they produce the correct results according to what was put in. If we
put garbage in we want pristine identical garbage out.

The services are intended to be very light weight, and just connect things. Things that might have wildly different
parameters and outputs. So no heavy lifting there. There are a few tests to see that the scenarios
from Boston_0_512 are accessible so there is some functionality.

Heuristics and children are shared between searches so they should be tested more to give correct results in
all situations.

Logging version of fringe was tested to output messages.

Thread versions of searches were tested to output correct amount and type of signals during a sample search. There should be more testing that
the payloads matched.