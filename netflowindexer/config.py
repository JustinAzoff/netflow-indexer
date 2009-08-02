import ConfigParser
import datetime

def read_config(fn):
    now = datetime.datetime.now()
    defaults = {
        'year':     str(now.year),
        'month':    "%02d" % now.month,
        'day':      "%02d" % now.day,
        'hour':     "%02d" % now.hour,
    }
    c = ConfigParser.ConfigParser(defaults=defaults)
    c.read(fn)
    return dict(c.items("nfi"))

if __name__ == "__main__":
    import pprint, sys
    pprint.pprint(read_config(sys.argv[1]))
