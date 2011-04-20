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
