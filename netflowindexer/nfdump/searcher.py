import datetime
import os
import subprocess

from netflowindexer.base.searcher import BaseSearcher
from netflowindexer import util

class NFDUMPSearcher(BaseSearcher):
    def docid_to_date(self, fn):
        """turn /data/nfsen/profiles/live/podium/nfcapd.2009030110 into
        a date of 2009-03-01 10:00"""
        t = fn[-10:]
        return util.strptime(t,'%Y%m%d%H')

    def any_ipv6(self, ips):
        return bool([1 for ip in ips if ':' in ip])

    def show(self, doc, filter, mode=None):
        start = doc + '00'
        end = os.path.basename(doc) + '55'

        command = ["nfdump", "-q"]

        if mode=="pipe":
            command.extend(["-o", "pipe"])
        if self.need_ipv6:
            command.append("-6")
        command.extend(["-R", start, end])
        command.append(filter)

        for line in subprocess.Popen(command, stdout=subprocess.PIPE).stdout:
            yield line.rstrip()

    def search(self, ips, dump=False, filter=None, mode=None):
        ip_filter = 'ip in [%s]' % ' '.join(ips)
        if filter:
            ip_filter = "%s AND (%s)" % (ip_filter, filter)

        self.need_ipv6 = self.any_ipv6(ips)

        docs = self.search_ips(ips)
        if not dump:
            for doc in docs:
                yield self.docid_to_date(doc)
        else:
            for doc in docs:
                for line in self.show(doc, ip_filter, mode):
                    yield line

searcher_class = NFDUMPSearcher
