API
===

Searching with the API
-----------------------


.. autoclass:: netflowindexer.main.Searcher
    :members:

Example
-------
The `Searcher` class can be used to search for records::

    from netflowindexer.main import Searcher
    s = Searcher("/spare/tmp/netflow/nfdump.ini")
    print s.list_databases()
    ['/spare/tmp/netflow/20110408.db']

    for record in s.search_all(['8.8.8.8']):
        print record
    2011-04-08 15:00:00
    2011-04-08 15:05:00
    2011-04-08 15:10:00
    2011-04-08 15:15:00
    2011-04-08 15:20:00
    ...

    for record in s.search_all(['8.8.8.8'], dump=True):
        print record
    2011-04-08 14:59:32.696     0.000 UDP     111.222.121.54:53241 ->          8.8.8.8:53           2      138     1
    2011-04-08 14:59:32.708     0.028 UDP            8.8.8.8:53    ->   111.222.121.54:53241        2      266     1
    2011-04-08 14:59:38.416     0.000 UDP     111.222.121.127:51528 ->          8.8.8.8:53          1       77     1
    2011-04-08 14:59:38.396     0.000 UDP            8.8.8.8:53    ->   111.222.121.127:51528       1      165     1
    2011-04-08 14:59:38.400     0.000 UDP     111.222.121.127:60043 ->          8.8.8.8:53          1       77     1
    2011-04-08 14:59:38.368     0.000 UDP            8.8.8.8:53    ->   111.222.121.127:60043       1      151     1
    2011-04-08 14:59:41.516     0.000 UDP     111.222.121.54:60128 ->          8.8.8.8:53           1       85     1
    2011-04-08 14:59:41.516     0.000 UDP     111.222.121.54:63357 ->          8.8.8.8:53           1       86     1

Searching with pynfdump
-----------------------

`pynfdump <http://packages.python.org/pynfdump/>`_ is another module I have written.

You can easily use netflow indexer with pynfdump::

    from netflowindexer.main import Searcher
    import pynfdump
    d=pynfdump.Dumper()
    s = Searcher("/spare/tmp/netflow/nfdump.ini")
    records = s.search_all(["8.8.8.8"], dump=True, filter='dst port 53', mode='pipe')
    for rec in d.parse_search(records):
        print rec['dstip'], rec['bytes']
    8.8.8.8 138
    8.8.8.8 77
    8.8.8.8 77
    8.8.8.8 85
    8.8.8.8 86
    8.8.8.8 85
    8.8.8.8 86
    8.8.8.8 86
    8.8.8.8 55
    8.8.8.8 55
    8.8.8.8 68

The above example used netflowindexer to find all flows to 8.8.8.8, then used
nfdump to filter it by 'dst port 53', and finally handed it off to pynfdump for
parsing.
