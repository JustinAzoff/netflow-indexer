#!/usr/bin/env python
import sys
import os
import glob

from netflowindexer.searcher.base import search

def main():
    from optparse import OptionParser
    parser = OptionParser(usage = "usage: %prog db [options] [ips]")
    parser.add_option("-d", "--extract", dest="extract", action="store_true", default=None,
        help="run flow-extract, don't just print the filenames")
    parser.add_option("-f", "--filter", dest="filter", action="store", default='',
        help="filter to use for flow-extract")

    (options, args) = parser.parse_args()

    if len(args) < 2:
        parser.print_help()
        sys.exit(1)

    db = args[0]
    ips = args[1:]
    f = options.filter
    ip_filter = ' or '.join('host = %s' % ip for ip in ips)
    if f:
        ip_filter = "(%s) and (%s)" % (ip_filter, options.filter)

    docs = sorted(list(search(db,ips)))
    if not options.nfdump:
        for doc in docs:
            print doc
    else:
        for doc in docs:
            os.system("flow-cat %s* | flow-extract -n -e %s {print}" % (doc, ip_filter))
