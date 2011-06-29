import datetime
import os

from netflowindexer.base.searcher import BaseSearcher

class NFDUMPSearcher(BaseSearcher):
    def docid_to_date(self, fn):
        """turn /data/nfsen/profiles/live/podium/nfcapd.2009030110 into
        a date of 2009-03-01 10:00"""
        t = fn[-10:]
        return datetime.datetime.strptime(t,'%Y%m%d%H')

    def any_ipv6(self, ips):
        return bool([1 for ip in ips if ':' in ip])

    def show(self, doc, filter, mode=None):
        start = doc + '00'
        end = os.path.basename(doc) + '55'

        pipe = ""
        if mode=="pipe":
            pipe = "-o pipe"

        for line in os.popen("nfdump %s %s -q -R %s:%s '%s'"  % (self.ipv6_flag, pipe, start,end, filter)):
            yield line.rstrip()

    def search(self, ips, dump=False, filter=None, mode=None):
        ip_filter = 'ip in [%s]' % ' '.join(ips)
        if filter:
            ip_filter = "%s AND (%s)" % (ip_filter, filter)

        self.ipv6_flag = ""
        if self.any_ipv6(ips):
            self.ipv6_flag = "-6"

        docs = self.search_ips(ips)
        if not dump:
            for doc in docs:
                yield self.docid_to_date(doc)
        else:
            for doc in docs:
                for line in self.show(doc, ip_filter, mode):
                    yield line

searcher_class = NFDUMPSearcher
