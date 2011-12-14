import glob
import os
import shutil
from netflowindexer import config
from netflowindexer.util import split_commas

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
    parser.add_option("-f", "--full-index", dest="full", action="store_true", default=False,
        help="Index all files matching allfileglob instead of fileglob")

    (options, args) = parser.parse_args()
    if not args:
        parser.print_help()
        return 1

    the_glob = options.full and 'allfileglob' or 'fileglob'

    cfgdata = config.read_config(args[0])

    files = sorted(glob.glob(cfgdata[the_glob]))
    if not files and not options.full:
        print "No files matched 'fileglob', perhaps you need --full-index?"
        return 1

    return do_index(cfgdata['indexer'], cfgdata, files)

def get_searcher(indexer_type):
    mod = __import__('netflowindexer.%s' % indexer_type)
    mod = getattr(mod, indexer_type)
    searcher = mod.searcher.searcher_class
    return searcher

class Searcher:
    """Create a new searcher instance.  Call with the path to the ini file"""
    def __init__(self, ini_file):
        self.cfgdata = config.read_config(ini_file)
        self.searcher = get_searcher(self.cfgdata['indexer'])

    def list_databases(self):
        """Return a list of database files in the 'dbpath' directory"""
        return sorted(glob.glob(self.cfgdata['dbpath'] + "/*.db"))

    def search(self, database, ips, dump=False, filter=None, mode=None):
        """Search a specific database file

        :param database: The full path to a database file.
        :param ips: a list of ip addresses to search for.
        :param dump: if True dump the full netflow records, otherwise just the seen timeslots
        :param filter: optional additional netflow search filter to be used when dump=True
        :param mode: set to 'pipe' to have nfdump list pipe delimited records
        """
        s = self.searcher(database)
        s.cfgdata = self.cfgdata
        for rec in s.search(ips, dump, filter, mode):
            yield rec

    def search_all(self, ips, dump=False, filter=None, mode=None):
        """Search all database files. Takes the same parameters as :func:`search`"""
        for db in self.list_databases():
            for rec in self.search(db, ips, dump, filter, mode):
                yield rec

def output_records(records, columns, dump):
    if dump:
        for r in records:
            print r
        return

    if not columns:
        columns = ['time']
    else:
        columns = split_commas(columns)

    for r in records:
        print ' '.join(str(getattr(r, c)) for c in columns)

def search():
    from optparse import OptionParser
    parser = OptionParser(usage = "usage: %prog indexer.ini database.db [searcher_options] IP...")
    parser.add_option("-d", "--dump", dest="dump", action="store_true", default=False,
        help="dump the flows, don't just print the filenames")
    parser.add_option("-f", "--filter", dest="filter", action="store", default='',
        help="filter to use when dumping flows with the -d option")
    parser.add_option("-c", "--columns", dest="columns", action="append",
        help="comma separated fields to include, default=time")

    (options, args) = parser.parse_args()
    ini = args and  args[0]
    db = len(args) > 1 and args[1]
    ips = len(args) > 2 and args[2:]
    if not (ini and db and ips):
        parser.print_help()
        return 1

    searcher = Searcher(ini)
    records = searcher.search(db, ips, options.dump, options.filter)
    output_records(records, options.columns, options.dump)

def search_all():
    from optparse import OptionParser
    parser = OptionParser(usage = "usage: %prog indexer.ini [searcher_options] IP...")
    parser.add_option("-d", "--dump", dest="dump", action="store_true", default=False,
        help="dump the flows, don't just print the filenames")
    parser.add_option("-f", "--filter", dest="filter", action="store", default='',
        help="filter to use when dumping flows with the -d option")
    parser.add_option("-c", "--columns", dest="columns", action="append",
        help="comma separated fields to include, default=time")

    (options, args) = parser.parse_args()
    if len(args) < 2:
        parser.print_help()
        return 1

    searcher = Searcher(args[0])
    ips = args[1:]
    records = searcher.search_all(ips, options.dump, options.filter)
    output_records(records, options.columns, options.dump)

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
    i = indexer(cfgdata)

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


