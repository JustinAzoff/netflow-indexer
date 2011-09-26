Configuration
=============

Netflow-indexer uses a small configuration file that setups the type of
indexer to use and the location of the files on disk.  It has the following
settings:

* indexer - the type of indexer to use. `nfdump`, `nfdump_full`, `flowtools`, or `flowtools_full`
* dbpath  - the path to save the indexes to
* fileglob - the shell glob that will expand to the flow data files for the
  current hour
* allfileglob - the shell glob that will expand to all flow data files
* pathregex - a regular expression or simple string used to extract metadata from flow file paths.


Example Configuration files
---------------------------

nfdump using full indexing(recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. include:: ../examples/nfdump_full.ini
    :literal:

nfdump
~~~~~~
.. include:: ../examples/nfdump.ini
    :literal:

flow-tools
~~~~~~~~~~
.. include:: ../examples/flowtools.ini
    :literal:


Cron
----
Netflow-indexer should be run from cron 5 minutes after every hour when using
the `nfdump` indexer and every 5 minutes when using the `nfdump_full` indexer::

    MAILTO=root
    PATH=/usr/local/python_env/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    45 0 * * *   cd /data/nfdump_xap/ && ./daily_compact > /dev/null
    */5  * * * * sleep 30;netflow-index-update  /data/nfdump_xap/nfdump.ini
    55 0 * * *   netflow-index-cleanup /data/nfdump_xap/nfdump.ini -d

Daily compaction
----------------

xapian allows you to compact an index for read-only use.  Compaction yields disk usage and speed improvements. 
daily compaction is a work in progress


examples/daily_compact.sh
~~~~~~~~~~~~~~~~~~~~~~~~~

.. include:: ../examples/daily_compact.sh
    :literal:

examples/xap_compact.sh
~~~~~~~~~~~~~~~~~~~~~~~

.. include:: ../examples/xap_compact.sh
    :literal:
