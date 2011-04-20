import datetime
import sys
import os

from netflowindexer.flowtools.searcher import FlowToolsSearcher

class FlowToolsFullSearcher(FlowToolsSearcher):
    def docid_to_date(self, fn):
        """turn /usr/local/var/db/flows/packeteer/2009/2009-03/2009-03-27/ft-v05.2009-03-27.1615 into
        a date of 2009-03-27 16:15"""
        t = fn[-15:]
        return datetime.datetime.strptime(t,'%Y-%m-%d.%H%M')

searcher_class = FlowToolsFullSearcher
