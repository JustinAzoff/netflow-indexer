#!/usr/bin/env python
import os
import subprocess

from netflowindexer.base.indexer import BaseIndexer

class BroIndexer(BaseIndexer):
    def get_ips(self, fn):
        ip_columns = map(int, self.cfg_data["ip_columns"].split(","))
        ips = set()
        add = ips.add
        for line in subprocess.Popen(["zcat", fn], stdout=subprocess.PIPE).stdout:
            if line.startswith("#"): continue
            parts = line.split("\t")
            if len(parts) < ip_columns[-1]:
                continue
            for col in ip_columns:
                add(parts[col])
        return ips

    def fn_to_db(self, fn):
        """turn /usr/local/opt/bro/logs/2013-11-14/conn-summary.22:05:46-22:08:52.log.gz into 2013-11-14.db"""
        day = fn.split("/")[-2]
        return "%s.db" % day

    def fn_to_docid(self, fn):
        return fn

indexer_class = BroIndexer
