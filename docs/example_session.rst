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

Search the index for 2009-03-29::

    justin@glenn:~$ host www.aol.com
    ...
    www-east.aol.com.aol.akadns.net A       64.12.168.33

    justin@glenn:~$ netflow-index-search -i nfdump /data/nfdump_xap/20090329.db 64.12.168.33
    /data/nfsen/profiles/live/podium/nfcapd.2009032905
    /data/nfsen/profiles/live/podium/nfcapd.2009032909
    /data/nfsen/profiles/live/podium/nfcapd.2009032911
    /data/nfsen/profiles/live/podium/nfcapd.2009032912
    /data/nfsen/profiles/live/podium/nfcapd.2009032913
    /data/nfsen/profiles/live/podium/nfcapd.2009032914

    real    0m0.075s
    user    0m0.052s
    sys     0m0.020s

This IP was present in the index for 6 of the 15 hours, so dumping all the netflow records
will be over twice as fast.

Searching for an IP that does not exist in the index is very fast::

    justin@glenn:~$ time netflow-index-search -i nfdump /data/nfdump_xap/20090329.db 1.2.3.4
    real    0m0.067s


Dumping data
------------

netflow-search-nfdump supports a -d option which automatically runs nfdump for you::

    justin@glenn:~$ netflow-index-search -i nfdump /data/nfdump_xap/20090329.db 64.12.168.33 -d 
    2009-03-29 05:03:54.792     1.260 TCP     xxx.xxx.xx.xxx:3392  ->     64.12.168.33:80    28 3160 1
    2009-03-29 05:03:56.052     0.328 TCP     xxx.xxx.xx.xxx:3398  ->     64.12.168.33:80     6 1786 1
    ...
