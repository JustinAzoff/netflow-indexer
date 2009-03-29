#!/usr/bin/env python
import os
import sys

from netflowindexer.indexer import base

class NFDUMPIndexer(base.BaseIndexer):
    def get_ips(self, fn):
        cmd = "nfdump -r '%s' -q -o pipe|cut -d '|' -f 10,15|tr '|' '\n'" % fn
        ips = set()
        for line in os.popen(cmd):
            ip = int(line)
            ips.add(ip)
        return ips
    def fn_to_db(self, fn):
        """turn /data/nfsen/profiles/live/podium/nfcapd.200903011030 into 20090301.db"""
        day = fn[-12:-4]
        return "%s.db" % day

    def fn_to_docid(self, fn):
        """turn /data/nfsen/profiles/live/podium/nfcapd.200903011030 into
                /data/nfsen/profiles/live/podium/nfcapd.2009030110"""
        
        return fn[:-2]

def main():
    i = NFDUMPIndexer()
    files = sys.argv[1:]
    i.index_files(files)
