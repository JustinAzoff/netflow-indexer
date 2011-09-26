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

def test_str_to_regex():
    tests = (
        ('/foo/:bar/baz', '/foo/(?P<bar>[^/]+)/baz'),
    )

    for input, output in tests:
        yield str_to_regex_case, input, output

def str_to_regex_case(input, output):
    eq_(str_to_regex(input), output)
