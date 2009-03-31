#!/usr/bin/env python
import sys
import os

from netflowindexer.base.searcher import search

def main(database, ips, dump=False, filter=None):
    ip_filter = 'ip in [%s]' % ' '.join(ips)
    if filter:
        ip_filter = "%s AND (%s)" % (ip_filter, filter)

    docs = sorted(list(search(database,ips)))
    if not dump:
        for doc in docs:
            print doc
    else:
        for doc in docs:
            start = doc + '00'
            end = os.path.basename(doc) + '55'
            os.system("nfdump -q -R %s:%s '%s'"  % (start,end, ip_filter))
