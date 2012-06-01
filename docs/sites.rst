Sites Using netflow-indexer
===========================

====================== ============  ========== =========== ==============
Site                   Netflow Size  Index size Index time  Search time
====================== ============  ========== =========== ==============
Masaryk University     5.6           56G        30 seconds  1-30 seconds
Indiana University     2.3T          91G        5 minutes   10-30 seconds
University of Waterloo 1.3T          109G       40 seconds  2-5 seconds
University of Scranton 255G          2.7G       5 seconds   1-10 seconds
University At Albany   91G           4.5G       <30 seconds 1-10 seconds
====================== ============  ========== =========== ==============


About `Search time`
~~~~~~~~~~~~~~~~~~~

There are 4 different kinds of searches:

#. A cold search returning zero results.
#. A cold search returning many results.
#. A warm search returning zero results.
#. A warm search returning many results.

Warm searches that return zero results are much faster than cold searches that
return many results.  Repeated warm searches finish in a fraction of a second
but that usage pattern is not a realistic benchmark.  I've tried to make
`Search time` above represent how long you would have to wait for typical
searches to finish.
