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
        words = []
        for ip in ips:
            if '/' in ip:
                net = self.expand_netmask(ip)
                #FIXME: raise exception?
                if len(net) < 300:
                    words.extend(net)
            else :
                words.append(self.convert_ip(ip))
        return self.do_search(words)

    def convert_ip(self, ip):
        return struct.pack(">L", IPy.IP(ip).int())

    def ips_from_network(self, network):
        #FIXME: a /24 should do two /23 searches, not 1/16
        net = struct.pack(">L", network.net().int())
        strip = network.prefixlen()/8
        prefix = net[:strip]

        ips = [i.term for i in self.database.allterms(prefix)]
        return ips

    def expand_netmask(self, netmask):
        """Expand netmask based on the terms in the database.
           Doesn't bother using the database for tiny networks"""
        network = IPy.IP(netmask)
        if len(network) < 32:
            return [struct.pack(">L", ip.int()) for ip in network]
        ips = self.ips_from_network(network)

        if network.prefixlen() not in (8,16,24):
            ips = [ip for ip in ips if IPy.IP(struct.unpack(">L", ip)[0]) in network]
        return ips

    def docid_to_date(self, fn):
        """turn /data/nfsen/profiles/live/podium/nfcapd.2009030110 into
        a date of 2009-03-01 10:00"""
        raise NotImplementedError()
