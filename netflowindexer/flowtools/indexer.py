#!/usr/bin/env python
import IPy
import os
import sys

from netflowindexer.base.indexer import BaseIndexer

class FlowToolsIndexer(BaseIndexer):
    def get_ips(self, fn):
        cmd = "flow-export -f2 < '%s' |cut -d ',' -f 11,12|tr ',' '\n'" % fn
        ips = set()
        f = os.popen(cmd)
        f.readline()# skip header
        f.readline()# skip header
        for line in f:
            ip = IPy.IP(line).int()
            ips.add(ip)
        return ips

    def fn_to_db(self, fn):
        """turn /usr/local/var/db/flows/packeteer/2009/2009-03/2009-03-27/ft-v05.2009-03-27.161500-0400 into 2009-03-27.db"""
        day = fn[-22:-12]
        return "%s.db" % day

    def fn_to_docid(self, fn):
        """turn /usr/local/var/db/flows/packeteer/2009/2009-03/2009-03-27/ft-v05.2009-03-27.161500-0400 into
                /usr/local/var/db/flows/packeteer/2009/2009-03/2009-03-27/ft-v05.2009-03-27.16
        """
        
        return fn[:-9]

indexer_class = FlowToolsIndexer
