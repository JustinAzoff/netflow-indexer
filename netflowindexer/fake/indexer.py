#!/usr/bin/env python
import os
import sys
import IPy

from netflowindexer.base.indexer import BaseIndexer

class FakeIndexer(BaseIndexer):
    def get_ips(self, fn):
        ips = set()
        for line in open(fn):
            ip = line.strip()
            ips.add(ip)
        return ips
    def fn_to_db(self, fn):
        """turn ips.2011-04-15-12.txt into ips.2011-04-15"""
        day = fn[-17:-7]
        return "%s.db" % day

    def fn_to_docid(self, fn):
        """turn ips.2011-04-15-12.txt to ips.2011-04-15-12"""
        
        return fn[:-4]

indexer_class = FakeIndexer

