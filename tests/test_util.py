from nose.tools import eq_
from netflowindexer.util import serialize_ip, deserialize_ip
def test_serde():
    ips = [
        "1.2.3.4",
        "fe80::225:64ff:fea2:2b2b",
    ]
    for ip in ips:
        yield serde_case, ip

def serde_case(ip):
    other = deserialize_ip(serialize_ip(ip))
    eq_(ip,other)

from netflowindexer.util import str_to_regex
import re

def test_str_to_regex():
    tests = (
        ('/foo/:bar/baz', '/foo/(?P<bar>[^/]+)/baz'),
    )

    for input, output in tests:
        yield str_to_regex_case, input, output

def str_to_regex_case(input, output):
    eq_(str_to_regex(input), output)

def test_str_to_regex_usage():
    filename = "/data/nfsen/profiles/live/podium/nfcapd.201109010000"

    regex = str_to_regex("profiles/:profile/:source/nfcapd")

    groups = re.search(regex, filename).groupdict()
    eq_(groups['profile'], 'live')
    eq_(groups['source'], 'podium')

from netflowindexer.util import split_commas

def test_split_commas():
    expected = ['a','b','c']
    tests = (
        ['a,b,c'],
        ['a','b','c'],
        ['a', 'b,c'], 
    )
    for t in tests:
        yield split_commas_case, t, expected

def split_commas_case(input, output):
    eq_(split_commas(input), output)
