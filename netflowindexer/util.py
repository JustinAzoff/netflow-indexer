from socket import inet_pton, inet_aton, inet_ntop, inet_ntoa, AF_INET6, error
def serialize_ip(ip):
    try :
        if ':' in ip:
            return inet_pton(AF_INET6, ip)
        else:
            return inet_aton(ip)
    except error:
        return None


def deserialize_ip(bytes):
    if len(bytes) == 4:
        return inet_ntoa(bytes)
    else:
        return inet_ntop(AF_INET6, bytes)

import datetime, time
def strptime_24(str, fmt):
    t = time.strptime(str, fmt)
    return datetime.datetime(*t[:6])

#strptime compatibility for python 2.4
if hasattr(datetime.datetime, 'strptime'):
    strptime = datetime.datetime.strptime
else:
    strptime = strptime_24


import re
def str_to_regex(input):
    """Convert a string like /path/to/:profile/foo/bar into a regex that will
    extract "profile"
    """
    def _sub(match):
        key = match.groups()[0]
        return '(?P<%s>[^/]+)' % key

    return re.sub(":([^/]+)", _sub, input)

def split_commas(input):
    output = []
    for x in input:
        output.extend(x.split(","))
    return output
