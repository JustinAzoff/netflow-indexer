Configuration
=============

Netflow-indexer uses a small configuration file that setups the type of
indexer to use and the location of the files on disk.  It has the following
settings:

* indexer - the type of indexer to use. `nfdump` or `flowtools`
* dbpath  - the path to save the indexes to
* fileglob - the shell glob that will expand to the flow data files for the
  current hour

Example Configuration files
---------------------------

nfdump
~~~~~~
.. include:: ../examples/nfdump.ini
    :literal:


flow-tools
~~~~~~~~~~
.. include:: ../examples/flowtools.ini
    :literal:


Cron
====
Netflow-indexer should be run from cron 5 minutes after every hour::

    5 * * * * netflow-index-update /data/nfdump_xap/nfdump.ini > /dev/null
