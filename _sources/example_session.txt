Example Session
===============

Indexing data
-------------

Tell the netflow indexer to index the current netflow files::

    justin@glenn:~$ netflow-index-update /data/nfdump_xap/nfdump.ini
    * /data/nfsen/profiles/live/podium/nfcapd.2009032900
    * /data/nfsen/profiles/live/podium/nfcapd.2009032901
    * /data/nfsen/profiles/live/podium/nfcapd.2009032902
    * /data/nfsen/profiles/live/podium/nfcapd.2009032903
    * /data/nfsen/profiles/live/podium/nfcapd.2009032904
    * /data/nfsen/profiles/live/podium/nfcapd.2009032905
    * /data/nfsen/profiles/live/podium/nfcapd.2009032906
    * /data/nfsen/profiles/live/podium/nfcapd.2009032907
    * /data/nfsen/profiles/live/podium/nfcapd.2009032908
    * /data/nfsen/profiles/live/podium/nfcapd.2009032909
    * /data/nfsen/profiles/live/podium/nfcapd.2009032910
    * /data/nfsen/profiles/live/podium/nfcapd.2009032911
    * /data/nfsen/profiles/live/podium/nfcapd.2009032912
    * /data/nfsen/profiles/live/podium/nfcapd.2009032913
    * /data/nfsen/profiles/live/podium/nfcapd.2009032914
    read /data/nfsen/profiles/live/podium/nfcapd.200903291400 in 1.3 seconds
    read /data/nfsen/profiles/live/podium/nfcapd.200903291405 in 1.3 seconds
    read /data/nfsen/profiles/live/podium/nfcapd.200903291410 in 1.4 seconds
    read /data/nfsen/profiles/live/podium/nfcapd.200903291415 in 1.4 seconds
    read /data/nfsen/profiles/live/podium/nfcapd.200903291420 in 1.4 seconds
    read /data/nfsen/profiles/live/podium/nfcapd.200903291425 in 1.3 seconds
    loading data into xapian took 8.8 seconds


Hours 00 through 13 are skipped because they are already fully indexed.

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
Searching the 30 day index takes only slightly longer and returns the same results

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
