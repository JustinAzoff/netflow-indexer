from netflowindexer.base import searcher
from netflowindexer.util import serialize_ip

def test_basic_search():
    s = searcher.BaseSearcher('tests/2011-04-15.db')
    assert(len(list(s.search_ips(["1.2.3.4"]))))==1
    assert(len(list(s.search_ips(["9.9.9.9"]))))==0

def test_ipv6_search():
    s = searcher.BaseSearcher('tests/2011-04-15.db')
    assert(len(list(s.search_ips(["2001:4860:800f::68"]))))==1
    assert(len(list(s.search_ips(["2001:4860:800f::62"]))))==0

def test_netmask_expand():
    s = searcher.BaseSearcher('tests/2011-04-15.db')

    expanded = s.expand_netmask("1.2.3.0/24")
    print expanded
    assert expanded == [serialize_ip(ip) for ip in ["1.2.3.4", "1.2.3.5", "1.2.3.6"]]

def test_netmask_expand_23():
    s = searcher.BaseSearcher('tests/2011-04-15.db')

    expanded = s.expand_netmask("3.3.2.0/23")
    print expanded
    assert expanded == [serialize_ip("3.3.3.99")]

def test_netmask_expand_ipv6():
    s = searcher.BaseSearcher('tests/2011-04-15.db')

    expanded = s.expand_netmask("2001:4860::/32")
    print expanded
    assert expanded == [serialize_ip("2001:4860:800f::68")]
