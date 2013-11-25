import gzip
import os
from netflowindexer.base.searcher import BaseSearcher
from netflowindexer import util
import re

class BroSearcher(BaseSearcher):
    def docid_to_date(self, fn):
        """turn ...logs/2013-11-14/conn.22:05:46-22:08:52.log.gz into
        a date of 2009-03-27 16:00"""
        d = fn.split("/")[-2]
        h = fn[-24:-22]
        t = "%s.%s" % (d, h)
        return util.strptime(t,'%Y-%m-%d.%H')

    def show(self, doc, ips):
        ips = [ip.replace(".", "\.") for ip in ips]
        inner = "|".join(ips)
        rex = re.compile("\t(%s)\t" % inner)

        f = gzip.open(doc)
        for line in f:
            if rex.search(line):
                yield line.rstrip()
        f.close()

    def search(self, ips, dump=False, filter=None, mode=None):
        docs = self.search_ips(ips)
        if not dump:
            for doc in docs:
                yield self.docid_to_searchresult(doc)
        else:
            for doc in docs:
                for line in self.show(doc, ips):
                    yield line

searcher_class = BroSearcher
