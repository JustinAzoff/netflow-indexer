import glob
import os
import shutil
from netflowindexer import config

def get_indexer(indexer_type):
    mod = __import__('netflowindexer.%s' % indexer_type)
    mod = getattr(mod, indexer_type)
    indexer = mod.indexer.indexer_class
    return indexer

def do_index(indexer_type, cfg_data, files):
    indexer = get_indexer(indexer_type)

    i = indexer(cfg_data)
    return i.index_files(files)

def index():
    from optparse import OptionParser
    parser = OptionParser(usage = "usage: %prog indexer.ini")

    (options, args) = parser.parse_args()
    if not args:
        parser.print_help()
        return 1
    cfgdata = config.read_config(args[0])

    files = sorted(glob.glob(cfgdata['fileglob']))

    return do_index(cfgdata['indexer'], cfgdata, files)

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

def search_all():
    from optparse import OptionParser
    parser = OptionParser(usage = "usage: %prog indexer.ini [searcher_options] IP...")
    parser.add_option("-d", "--dump", dest="dump", action="store_true", default=False,
        help="dump the flows, don't just print the filenames")
    parser.add_option("-f", "--filter", dest="filter", action="store", default='',
        help="filter to use when dumping flows with the -d option")

    (options, args) = parser.parse_args()
    if len(args) < 2:
        parser.print_help()
        return 1

    cfgdata = config.read_config(args[0])
    ips = args[1:]
    for db in sorted(glob.glob(cfgdata['dbpath'] + "/*.db")):
        do_search(cfgdata['indexer'], db, ips, options.dump, options.filter)

def cleanup():
    from optparse import OptionParser

    parser = OptionParser(usage = "usage: %prog indexer.ini")
    parser.add_option("-d", "--delete", dest="delete", action="store_true", default=False,
        help="Delete old database files, don't just print a report")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.print_help()
        return 1
    cfgdata = config.read_config(args[0])

    indexer = get_indexer(cfgdata['indexer'])
    i = indexer('')

    databases = sorted([x for x in os.listdir(cfgdata['dbpath']) if x.endswith(".db")])

    data_files = glob.glob(cfgdata['allfileglob'])
    needed_databases = set([i.fn_to_db(f) for f in data_files])

    to_delete = [x for x in databases if x not in needed_databases]

    for x in to_delete:
        full_path = os.path.join(cfgdata['dbpath'], x)
        if options.delete:
            print "Deleting", full_path
            shutil.rmtree(full_path)
        else:
            print "Need to delete:", full_path
