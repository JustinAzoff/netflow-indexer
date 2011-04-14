#!/usr/bin/env python
import sys
import os
import xapian
import IPy

import struct

class BaseSearcher:
    def __init__(self, db):
        self.database = xapian.Database(db)

    def do_search(self, words):
        enquire = xapian.Enquire(self.database)
        query = xapian.Query(xapian.Query.OP_OR, words)

        enquire.set_query(query)
        matches = enquire.get_mset(0, 2000)

        for match in matches:
            doc = match.document.get_data()
            yield doc

    def search_ips(self, ips):
        words = [struct.pack(">L", IPy.IP(ip).int()) for ip in ips]
        return self.do_search(words)

    def docid_to_date(self, fn):
        """turn /data/nfsen/profiles/live/podium/nfcapd.2009030110 into
        a date of 2009-03-01 10:00"""
        raise NotImplementedError()
