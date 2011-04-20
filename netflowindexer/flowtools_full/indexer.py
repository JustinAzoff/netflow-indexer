from netflowindexer.flowtools.indexer import FlowToolsIndexer

class FlowToolsFullIndexer(FlowToolsIndexer):
    def fn_to_docid(self, fn):
        """turn /usr/local/var/db/flows/packeteer/2009/2009-03/2009-03-27/ft-v05.2009-03-27.161500-0400 into
                /usr/local/var/db/flows/packeteer/2009/2009-03/2009-03-27/ft-v05.2009-03-27.1615
        
        return fn[:-7]

indexer_class = FlowToolsFullIndexer
