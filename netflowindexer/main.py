import glob
from netflowindexer import config

def get_indexer(indexer_type):
    mod = __import__('netflowindexer.%s' % indexer_type)
    mod = getattr(mod, indexer_type)
    indexer = mod.indexer.indexer_class
    return indexer

def do_index(indexer_type, out_dir, files):
    indexer = get_indexer(indexer_type)

    i = indexer(out_dir)
    return i.index_files(files)

def index():
    from optparse import OptionParser
    parser = OptionParser(usage = "usage: %prog indexer.ini")

    (options, args) = parser.parse_args()
    if not args:
        parser.print_help()
        return 1
    cfgdata = config.read_config(args[0])

    files = glob.glob(cfgdata['fileglob'])

    return do_index(cfgdata['indexer'], cfgdata['dbpath'], files)

def get_searcher(indexer_type):
    mod = __import__('netflowindexer.%s' % indexer_type)
    mod = getattr(mod, indexer_type)
    searcher = mod.searcher.main
    return searcher

def do_search(indexer_type, database, ips, dump=None,filter=None):
    searcher = get_searcher(indexer_type)
    return searcher(database, ips, dump, filter)

def search():
    from optparse import OptionParser
    parser = OptionParser(usage = "usage: %prog -i indexer [searcher_options] database.db IP...")
    parser.add_option("-i", "--indexer", dest="indexer", action="store",
        help="indexer to use")
    parser.add_option("-d", "--dump", dest="dump", action="store_true", default=False,
        help="dump the flows, don't just print the filenames")
    parser.add_option("-f", "--filter", dest="filter", action="store", default='',
        help="filter to use when dumping flows with the -d option")

    (options, args) = parser.parse_args()
    if not options.indexer:
        parser.print_help()
        return 1

    return do_search(options.indexer, args[0], args[1:], options.dump, options.filter)
