#!/usr/bin/env python
import os
import sys
import xapian
import struct
import itertools
import time

from socket import inet_pton, inet_aton, AF_INET6

class BaseIndexer:
    def __init__(self, cfg_data):
        self.database = None
        self.db_fn = None
        self.doc_count = 0
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
        if ':' in ip:
            return inet_pton(AF_INET6, ip)
        else:
            return inet_aton(ip)

    def get_ips(self, fn):
        raise NotImplementedError()

    def get_bytes(self, fn):
        ips = self.get_ips(fn)
        return map(self.dump_ip, ips)

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
            if self.database:
                self.maybe_flush(True)
            self.database = xapian.WritableDatabase(db_fn, xapian.DB_CREATE_OR_OPEN)
        return self.database

    def maybe_flush(self, force=False):
        self.doc_count += 1
        if self.doc_count == 12*3 or force:
            st = time.time()
            self.database.flush()
            print "Flush took %0.1f seconds." % (time.time() - st)
            self.doc_count = 0

    def index_files(self, fns):
        for docid, files in itertools.groupby(fns, self.fn_to_docid):
            #print '*', docid
            self.real_index_files(list(files))
        self.maybe_flush(True)

    def real_index_files(self, fns):
        begin = time.time()
        last_fn = fns[-1]
        database = self.open_db(last_fn)
        #if the last file is already indexed, nothing to do
        if self.has_document("fn:%s" % last_fn):
            return
        if len(fns) == 1:
            st = time.time()
            ips = self.get_bytes(fns[0])
            print "read %s in %0.1f seconds. %d ips." % (fns[0], time.time() - st, len(ips))
        else:
            ips = set()
            for fn in fns:
                st = time.time()
                ips.update(self.get_bytes(fn))
                print "read %s in %0.1f seconds. %d ips." % (fn, time.time() - st, len(ips))

        doc = xapian.Document()

        map(doc.add_term, ips)

        for fn in fns:
            doc.add_term("fn:%s" % fn)

        #docid is the hour part of the filename
        docid = self.fn_to_docid(fn)
        doc.set_data(docid)
        key = "fn:%s" % docid
        doc.add_term(key)
        database.replace_document(key, doc)
        self.maybe_flush()

        #print 'loading data into xapian took %0.1f seconds. %0.1f total' % (time.time() - st, time.time() - begin)
