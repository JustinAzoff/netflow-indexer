import datetime
import sys
import os

from netflowindexer.nfdump.searcher import NFDUMPSearcher

class NFDUMPFullSearcher(NFDUMPSearcher):
    def docid_to_date(self, fn):
        """turn /data/nfsen/profiles/live/podium/nfcapd.200903011020 into
        a date of 2009-03-01 10:20"""
        t = fn[-12:]
        return datetime.datetime.strptime(t,'%Y%m%d%H%M')

    def show(self, doc, filter):
        os.system("nfdump %s -q -r %s '%s'"  % (self.ipv6_flag, doc, filter))

searcher_class = NFDUMPFullSearcher
