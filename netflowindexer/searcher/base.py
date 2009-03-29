#!/usr/bin/env python
import sys
import os
import xapian
import IPy

import struct

def do_search(database, words):
    enquire = xapian.Enquire(database)
    q = []
    query = xapian.Query(xapian.Query.OP_OR, words)

    enquire.set_query(query)
    matches = enquire.get_mset(0, 2000)

    for match in matches:
        doc = match[xapian.MSET_DOCUMENT].get_data()
        yield doc

def search(db, words):
    database = xapian.Database(db)
    ips = [struct.pack("<L", IPy.IP(word).int()) for word in words]
    for doc in do_search(database, ips):
        yield doc
