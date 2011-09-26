import ConfigParser
import datetime

from netflowindexer.util import str_to_regex
import re

def read_config(fn):
    now = datetime.datetime.now() - datetime.timedelta(minutes=10)

    defaults = {
        'year':     str(now.year),
        'month':    "%02d" % now.month,
        'day':      "%02d" % now.day,
        'hour':     "%02d" % now.hour,
    }
    c = ConfigParser.ConfigParser(defaults=defaults)
    c.read(fn)
    config = dict(c.items("nfi"))
    if 'pathregex' in config:
        if ':' in config['pathregex']:
            config['pathregex'] = str_to_regex(config['pathregex'])
        config['pathregex'] = re.compile(config['pathregex'])

    return config

if __name__ == "__main__":
    import pprint, sys
    pprint.pprint(read_config(sys.argv[1]))
