#!/usr/bin/env python
import datetime
import sys
import os

from netflowindexer.base.searcher import BaseSearcher

class NFDUMPSearcher(BaseSearcher):
    def docid_to_date(self, fn):
        """turn /data/nfsen/profiles/live/podium/nfcapd.2009030110 into
        a date of 2009-03-01 10:00"""
        t = fn[-10:]
        return datetime.datetime.strptime(t,'%Y%m%d%H')

    def search(self, ips, dump=False, filter=None):
        ip_filter = 'ip in [%s]' % ' '.join(ips)
        if filter:
            ip_filter = "%s AND (%s)" % (ip_filter, filter)

        docs = sorted(list(self.search_ips(ips)))
        if not dump:
            for doc in docs:
                print self.docid_to_date(doc)
        else:
            for doc in docs:
                start = doc + '00'
                end = os.path.basename(doc) + '55'
                os.system("nfdump -q -R %s:%s '%s'"  % (start,end, ip_filter))

searcher_class = NFDUMPSearcher
