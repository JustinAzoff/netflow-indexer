import datetime
import sys
import os

from netflowindexer.base.searcher import BaseSearcher

class FakeSearcher(BaseSearcher):
    def docid_to_date(self, fn):
        """turn ips.2011-04-15-12.txt into a date"""
        t = fn[-13:]
        return datetime.datetime.strptime(t,'%Y-%m-%d-%H')

    def search(self, ips, dump=False, filter=None):

        docs = self.search_ips(ips)
        if not dump:
            for doc in docs:
                print self.docid_to_date(doc)
        else:
            for doc in docs:
                os.system("cat " + doc)

searcher_class = FakeSearcher
