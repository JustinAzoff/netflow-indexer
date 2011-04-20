from netflowindexer.nfdump.indexer import NFDUMPIndexer

class NFDUMPFullIndexer(NFDUMPIndexer):
    def fn_to_docid(self, fn):
        """turn /data/nfsen/profiles/live/podium/nfcapd.200903011030 into
                /data/nfsen/profiles/live/podium/nfcapd.200903011030"""
        
        return fn

indexer_class = NFDUMPFullIndexer
