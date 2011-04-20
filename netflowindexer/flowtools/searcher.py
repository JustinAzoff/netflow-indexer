import datetime
import sys
import os
from netflowindexer.base.searcher import BaseSearcher

class FlowToolsSearcher(BaseSearcher):
    def docid_to_date(self, fn):
        """turn /usr/local/var/db/flows/packeteer/2009/2009-03/2009-03-27/ft-v05.2009-03-27.16 into
        a date of 2009-03-27 16:00"""
        t = fn[-13:]
        return datetime.datetime.strptime(t,'%Y-%m-%d.%H')

    def search(self, ips, dump=False, filter=None):
        def make_filter(ip):
            if '/' in ip:
                return 'net = %s' % ip
            else :
                return 'host = %s' % ip

        ip_filter = ' or '.join(make_filter(ip) for ip in ips)
        if filter:
            ip_filter = "(%s) and (%s)" % (ip_filter, filter)

        docs = sorted(list(self.search_ips(ips)))
        if not dump:
            for doc in docs:
                print self.docid_to_date(doc)
        else:
            for doc in docs:
                os.system("flow-cat %s* | flow-extract -n -e '%s {print}'" % (doc, ip_filter))

searcher_class = FlowToolsSearcher
