#!/usr/bin/env python
import sys
import os
import glob

from netflowindexer.base.searcher import search

def main(database, ips, dump=False, filter=None):
    ip_filter = ' or '.join('host = %s' % ip for ip in ips)
    if filter:
        ip_filter = "(%s) and (%s)" % (ip_filter, filter)

    docs = sorted(list(search(database,ips)))
    if not dump:
        for doc in docs:
            print doc
    else:
        for doc in docs:
            os.system("flow-cat %s* | flow-extract -n -e '%s {print}'" % (doc, ip_filter))
