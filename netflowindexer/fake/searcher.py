from netflowindexer.base.searcher import BaseSearcher
from netflowindexer import util
import IPy

class FakeSearcher(BaseSearcher):
    def docid_to_date(self, fn):
        """turn ips.2011-04-15-12.txt into a date"""
        t = fn[-13:]
        return util.strptime(t,'%Y-%m-%d-%H')

    def show(self, doc, ips, mode=None):
        for l in open(doc + ".txt"):
            l = l.rstrip()
            if any(l in ip for ip in ips):
                yield l
        

    def search(self, ips, dump=False, filter=None,mode=None):

        docs = self.search_ips(ips)
        if not dump:
            for doc in docs:
                yield self.docid_to_searchresult(doc)
        else:
            ips = [IPy.IP(ip) for ip in ips]
            for doc in docs:
                for line in self.show(doc, ips):
                    yield line

searcher_class = FakeSearcher
