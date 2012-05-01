Example Session
===============

Indexing data
-------------

Tell the netflow indexer to index the current netflow files
For this example I deleted todays index so it can be re-created ::

    netflow@nf:~$ netflow-index-update  /data/nfdump_xap/nfdump.ini
    read /data/nfsen/profiles/live/podium/nfcapd.201205010000 in 2.4 seconds. 64501 ips.
    read /data/nfsen/profiles/live/podium/nfcapd.201205010005 in 2.5 seconds. 70830 ips.
    read /data/nfsen/profiles/live/podium/nfcapd.201205010010 in 3.8 seconds. 120925 ips.
    read /data/nfsen/profiles/live/podium/nfcapd.201205010015 in 2.7 seconds. 65676 ips.
    ...
    read /data/nfsen/profiles/live/podium/nfcapd.201205010240 in 1.3 seconds. 54040 ips.
    read /data/nfsen/profiles/live/podium/nfcapd.201205010245 in 1.3 seconds. 52391 ips.
    read /data/nfsen/profiles/live/podium/nfcapd.201205010250 in 1.2 seconds. 49993 ips.
    read /data/nfsen/profiles/live/podium/nfcapd.201205010255 in 1.2 seconds. 52161 ips.
    Flush took 7.4 seconds.
    ...
    read /data/nfsen/profiles/live/podium/nfcapd.201205011615 in 7.4 seconds. 159399 ips.
    read /data/nfsen/profiles/live/podium/nfcapd.201205011620 in 7.1 seconds. 155225 ips.
    read /data/nfsen/profiles/live/podium/nfcapd.201205011625 in 5.7 seconds. 110510 ips.
    Flush took 28.9 seconds.

Running the indexer when more data is available does an incremental update::

    netflow@nf:~$ netflow-index-update  /data/nfdump_xap/nfdump.ini
    read /data/nfsen/profiles/live/podium/nfcapd.201205011630 in 3.7 seconds. 110257 ips.
    read /data/nfsen/profiles/live/podium/nfcapd.201205011635 in 3.7 seconds. 116742 ips.
    read /data/nfsen/profiles/live/podium/nfcapd.201205011640 in 4.2 seconds. 107927 ips.
    Flush took 7.0 seconds.
    netflow@nf:~$ netflow-index-update  /data/nfdump_xap/nfdump.ini
    netflow@nf:~$ 

When performing an index for the first time you should use the `--full-index`
or `-f` option to index all the data.  By default netflow-indexer only tries
indexing files that match `fileglob`::

    netflow-index-update /data/nfdump_xap/nfdump.ini --full-index

Searching the index
-------------------

Search the index for 2011-04-18::

    # 59.124.163.60 is an address that just scanned us
    remote@nf:~$ time netflow-index-search /data/nfdump_xap/nfdump.ini /data/nfdump_xap/20110419.db 59.124.163.60
    2011-04-19 05:35:00
    2011-04-19 05:40:00
    2011-04-19 05:45:00
    2011-04-19 05:50:00
    2011-04-19 05:55:00
    2011-04-19 06:00:00
    2011-04-19 06:05:00
    2011-04-19 07:40:00
    2011-04-19 07:45:00
    2011-04-19 07:50:00
    2011-04-19 07:55:00

    real    0m0.072s

This output shows that it was present in the index in 11 5 minute chunks.
Searching the 30 day index takes only slightly longer and returns the same results::

    remote@nf:~$ time netflow-index-search-all /data/nfdump_xap/nfdump.ini 59.124.163.60

Searching for an IP that does not exist in the index is very fast::

    remote@nf:~$ netflow-index-search-all /data/nfdump_xap/nfdump.ini 9.254.9.254

    real    0m0.268s

Specifying output columns
-------------------------

`netflow-index-search` and `netflow-index-search-all` support a -c option which selects
what columns should be output. By default only `time` is output. The other
built-in field is `filename`.  Additional fields are made available by using
the `pathregex` configuration option. Columns can be selected by using two
methods::

    -c time -c filename

or::

    -c time,filename

Dumping data
------------

`netflow-index-search` and `netflow-index-search-all` support a -d option which
automatically runs the appropriate netflow tool for you::

    remote@nf:~$ time netflow-index-search-all /data/nfdump_xap/nfdump.ini 59.124.163.60 -d|head
    2011-04-19 05:38:36.468     1.696 TCP      59.124.163.60:39432 ->    123.123.2.245:22           4      192     1
    2011-04-19 05:38:36.468     1.776 TCP      59.124.163.60:50920 ->    123.123.2.246:22           4      192     1
    2011-04-19 05:38:36.468     1.428 TCP      123.123.2.245:22    ->    59.124.163.60:39432        4      237     1
    2011-04-19 05:38:36.472     0.828 TCP      59.124.163.60:36167 ->    123.123.2.247:22           3      152     1
    ...

You can also use the -f option to pass an additional filter::

    remote@nf:~$ netflow-index-search-all /data/nfdump_xap/nfdump.ini 59.124.163.60 -d -f 'not port 22'
