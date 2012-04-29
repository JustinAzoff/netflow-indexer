#!/usr/bin/env python
import os
import xapian
import IPy

from netflowindexer.util import serialize_ip, deserialize_ip

class SearchResult(dict):
    def __init__(self, filename, time, **kwargs):
        dict.__init__(self, kwargs)
        self.__dict__ = self
        self.filename = filename
        self.time = time

    def __str__(self):
        return str(self.time)

    def __repr__(self):
        others = ', '.join(["%s=%s" % (k,v) for (k,v) in self.items() if k not in ('filename','time')])
        if others:
            others = ", " + others
        s = "SearchResult(filename=%s, time=%s%s)" % (self.filename, self.time, others)
        return s

class BaseSearcher:
    def __init__(self, db):
        self.database = xapian.Database(db)

    def do_search(self, words):
        enquire = xapian.Enquire(self.database)
        query = xapian.Query(xapian.Query.OP_OR, words)

        enquire.set_query(query)
        matches = enquire.get_mset(0, 2000)

        results = []
        for match in matches:
            doc = match.document.get_data()
            results.append(doc)
        results.sort(key=os.path.basename)
        return results

    def search_ips(self, ips):
        words = []
        for ip in ips:
            if '/' in ip:
                net = self.expand_netmask(ip)
                #FIXME: raise exception?
                if len(net) < 300:
                    words.extend(net)
            else :
                words.append(serialize_ip(ip))
        return self.do_search(words)

    def ips_from_network(self, network):
        #FIXME: a /24 should do two /23 searches, not 1/16
        net = serialize_ip(str(network.net()))
        strip = network.prefixlen()/8
        prefix = net[:strip]

        ips = [i.term for i in self.database.allterms(prefix)]
        return ips

    def expand_netmask(self, netmask):
        """Expand netmask based on the terms in the database.
           Doesn't bother using the database for tiny networks"""
        network = IPy.IP(netmask)
        if network.len() < 32:
            return [serialize_ip(str(ip)) for ip in network]
        ips = self.ips_from_network(network)

        if network.prefixlen() % 8 !=0:
            ips = [ip for ip in ips if IPy.IP(deserialize_ip(ip)) in network]
        return ips

    def docid_to_date(self, fn):
        """turn /data/nfsen/profiles/live/podium/nfcapd.2009030110 into
        a date of 2009-03-01 10:00"""
        raise NotImplementedError()

    def docid_to_searchresult(self, fn):
        """return /data/nfsen/profiles/live/podium/nfcapd.2009030110 into an object containing
            filename - the full filename
            date - the parsed date
            any fields extracted from the pathregex
        """
        time = self.docid_to_date(fn)
        path_info = {}
        if 'pathregex' in self.cfgdata:
            path_info = self.cfgdata['pathregex'].search(fn).groupdict()
        return SearchResult(fn, time, **path_info)
