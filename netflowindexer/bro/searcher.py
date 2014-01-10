import subprocess
import os
from netflowindexer.base.searcher import BaseSearcher
from netflowindexer import util
import re
import datetime

class BroSearcher(BaseSearcher):
    def docid_to_date(self, fn):
        """turn ...logs/2013-11-14/conn.22:05:46-22:08:52.log.gz into
        a date of 2009-03-27 16:00"""
        d = fn.split("/")[-2]
        h = fn[-24:-22]
        t = "%s.%s" % (d, h)
        return util.strptime(t,'%Y-%m-%d.%H')

    def fix_ts(self, line):
        ts, rest = line.split("\t", 1)
        ts = datetime.datetime.fromtimestamp(float(ts)).isoformat()
        return '\t'.join((ts, rest))

    def show(self, doc, ips):
        ips = [ip.replace(".", "\.") for ip in ips]
        inner = "|".join(ips)
        rex = re.compile("\t(%s)\t" % inner)

        for line in subprocess.Popen(["zcat", doc], stdout=subprocess.PIPE).stdout:
            if rex.search(line):
                yield self.fix_ts(line.rstrip())

    def search(self, ips, dump=False, filter=None, mode=None):
        docs = self.search_ips(ips)
        if not dump:
            for doc in docs:
                yield self.docid_to_searchresult(doc)
            return

        all_ips = []
        for ip in ips:
            if '/' in ip:
                all_ips.extend(map(util.deserialize_ip, self.expand_netmask(ip)))
            else:
                all_ips.append(ip)
        for doc in docs:
            for line in self.show(doc, all_ips):
                yield line

searcher_class = BroSearcher
