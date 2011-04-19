#!/usr/bin/env python
import os
import sys

from netflowindexer.base.indexer import BaseIndexer

from struct import pack

class NFDUMPIndexer(BaseIndexer):
    def get_bytes(self, fn):
        cmd = "nfdump -r '%s' -q -o pipe" % fn
        ips = set()
        update = ips.update
        for line in os.popen(cmd):
            parts = line.split("|")
            if parts[6:9] != ['0','0','0']: #ipv6
                sa = pack(">LLLL", int(parts[6]),  int(parts[7]),  int(parts[8]),  int(parts[9]))
                da = pack(">LLLL", int(parts[11]), int(parts[12]), int(parts[13]), int(parts[14]))
            else:
                sa = pack(">L", int(parts[9]))
                da = pack(">L", int(parts[14]))
            update([sa,da])
        return ips
    def fn_to_db(self, fn):
        """turn /data/nfsen/profiles/live/podium/nfcapd.200903011030 into 20090301.db"""
        day = fn[-12:-4]
        return "%s.db" % day

    def fn_to_docid(self, fn):
        """turn /data/nfsen/profiles/live/podium/nfcapd.200903011030 into
                /data/nfsen/profiles/live/podium/nfcapd.2009030110"""
        
        return fn[:-2]

indexer_class = NFDUMPIndexer

