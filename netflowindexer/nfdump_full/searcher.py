import datetime
import sys
import os
import subprocess

from netflowindexer.nfdump.searcher import NFDUMPSearcher

class NFDUMPFullSearcher(NFDUMPSearcher):
    def docid_to_date(self, fn):
        """turn /data/nfsen/profiles/live/podium/nfcapd.200903011020 into
        a date of 2009-03-01 10:20"""
        t = fn[-12:]
        return datetime.datetime.strptime(t,'%Y%m%d%H%M')

    def show(self, doc, filter, mode=None):
        command = ["nfdump", "-q"]
        if mode=="pipe":
            command.extend(["-o", "pipe"])
        if self.need_ipv6:
            command.append("-6")
        command.extend(["-r", doc])
        command.append(filter)

        for line in subprocess.Popen(command, stdout=subprocess.PIPE).stdout:
            yield line.rstrip()

searcher_class = NFDUMPFullSearcher
