#!/usr/bin/env python
import os
import sys
import xapian
import struct
import itertools
import time


class BaseIndexer:
    def __init__(self, cfg_data):
        self.database = None
        self.db_fn = None
        self.out_dir = cfg_data['dbpath']
        self.flowpath = cfg_data['flowpath']

    def has_document(self, key):
        enquire = xapian.Enquire(self.database)
        query = xapian.Query(key)

        enquire.set_query(query)
        matches = enquire.get_mset(0, 2)

        for match in matches:
            return True
        return False

    def dump_ip(self, ip):
        return struct.pack(">L", ip.int())

    def get_ips(self, fn):
        raise NotImplementedError()

    def fn_to_db(self, fn):
        """turn /data/nfsen/profiles/live/podium/nfcapd.200903011030 into 20090301.db"""
        raise NotImplementedError()

    def fn_to_docid(self, fn):
        """turn /data/nfsen/profiles/live/podium/nfcapd.200903011030 into
                /data/nfsen/profiles/live/podium/nfcapd.2009030110"""
        raise NotImplementedError()

    def open_db(self, fn):
        db_fn = os.path.join(self.out_dir, self.fn_to_db(fn))
        if db_fn != self.db_fn:
            self.db_fn = db_fn
            self.database = xapian.WritableDatabase(db_fn, xapian.DB_CREATE_OR_OPEN)
        return self.database

    def index_files(self, fns):
        for docid, files in itertools.groupby(fns, self.fn_to_docid):
            print '*', docid
            self.real_index_files(list(files))

    def real_index_files(self, fns):
        last_fn = fns[-1]
        database = self.open_db(last_fn)
        #if the last file is already indexed, nothing to do
        if self.has_document("fn:%s" % last_fn):
            return
        ips = set()
        for fn in fns:
            st = time.time()
            #for r in pynfdump.search_file(fn):
            #    ips.add(self.dump_ip(r['srcip']))
            #    ips.add(self.dump_ip(r['dstip']))
            for ip in self.get_ips(fn):
                ips.add(struct.pack(">L", ip))
            print "read %s in %0.1f seconds" % (fn, time.time() - st)

        st = time.time()
        doc = xapian.Document()


        for ip in ips:
            doc.add_term(ip)

        for fn in fns:
            doc.add_term("fn:%s" % fn)

        #docid is the hour part of the filename
        docid = self.fn_to_docid(fn)
        doc.set_data(docid)
        key = "fn:%s" % docid
        doc.add_term(key)
        database.replace_document(key, doc)
        database.flush()

        print 'loading data into xapian took %0.1f seconds' % (time.time() - st)
