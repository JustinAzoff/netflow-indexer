import os
from netflowindexer.base.searcher import BaseSearcher
from netflowindexer import util

class FlowToolsSearcher(BaseSearcher):
    def docid_to_date(self, fn):
        """turn /usr/local/var/db/flows/packeteer/2009/2009-03/2009-03-27/ft-v05.2009-03-27.16 into
        a date of 2009-03-27 16:00"""
        t = fn[-13:]
        return util.strptime(t,'%Y-%m-%d.%H')

    def show(self, doc, filter):
        for line in os.popen("flow-cat %s* | flow-extract -n -e '%s {print}'" % (doc, filter)):
            yield line.rstrip()

    def search(self, ips, dump=False, filter=None, mode=None):
        def make_filter(ip):
            if '/' in ip:
                return 'net = %s' % ip
            else :
                return 'host = %s' % ip

        ip_filter = ' or '.join(make_filter(ip) for ip in ips)
        if filter:
            ip_filter = "(%s) and (%s)" % (ip_filter, filter)

        docs = self.search_ips(ips)
        if not dump:
            for doc in docs:
                yield self.docid_to_searchresult(doc)
        else:
            for doc in docs:
                for line in self.show(doc, ip_filter):
                    yield line

searcher_class = FlowToolsSearcher
