#!/usr/bin/env python
import sys
import os

from netflowindexer.base.searcher import search

def main(*args):
    from optparse import OptionParser
    parser = OptionParser(usage = "usage: %prog db [options] [ips]")
    parser.add_option("-d", "--nfdump", dest="nfdump", action="store_true", default=None,
        help="run nfdump, don't just print the filenames")
    parser.add_option("-f", "--filter", dest="filter", action="store", default='',
        help="filter to use for nfdump")

    (options, args) = parser.parse_args(list(args))

    if len(args) < 2:
        parser.print_help()
        sys.exit(1)

    db = args[0]
    ips = args[1:]
    f = options.filter
    if f:
        f = "AND %s" % options.filter

    docs = sorted(list(search(db,ips)))
    if not options.nfdump:
        for doc in docs:
            print doc
    else:
        for doc in docs:
            start = doc + '00'
            end = os.path.basename(doc) + '55'
            os.system("nfdump -q -R %s:%s 'ip in [%s] %s'"  % (start,end, ' '.join(ips), f))
