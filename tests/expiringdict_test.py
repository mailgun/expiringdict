from time import sleep

from mock import Mock, patch
from nose.tools import assert_raises, eq_, ok_

from expiringdict import ExpiringDict
try:
    from collections import OrderedDict
except ImportError:
    # Python < 2.7
    from ordereddict import OrderedDict

def test_create():
    assert_raises(AssertionError, ExpiringDict, max_len=1, max_age_seconds=-1)
    assert_raises(AssertionError, ExpiringDict, max_len=0, max_age_seconds=1)

    d = ExpiringDict(max_len=3, max_age_seconds=0.01)
    eq_(len(d), 0)


def test_basics():
    d = ExpiringDict(max_len=3, max_age_seconds=0.01)

    eq_(d.get('a'), None)
    d['a'] = 'x'
    eq_(d.get('a'), 'x')

    sleep(0.01)
    eq_(d.get('a'), None)

    d['a'] = 'y'
    eq_(d.get('a'), 'y')

    ok_('b' not in d)
    d['b'] = 'y'
    ok_('b' in d)

    sleep(0.01)
    ok_('b' not in d)

    # a is still in expiringdict, next values should expire it
    d['c'] = 'x'
    d['d'] = 'y'
    d['e'] = 'z'

    # dict if full
    ok_('c' in d)
    ok_('d' in d)

    d['f'] = '1'
    # c should gone after that
    ok_('c' not in d, 'Len of dict is more than max_len')

    # test __delitem__
    del d['e']
    ok_('e' not in d)

def test_auto_refresh():
    d = ExpiringDict(max_len=3, max_age_seconds=0.01, auto_refresh=True)
    d['a'] = 'x'
    eq_(d.get('a'), 'x')
    sleep(0.005)
    d['a']
    sleep(0.005)
    eq_(d.get('a'), 'x')
    sleep(0.01)
    eq_(d.get('a'), None)

    d = ExpiringDict(max_len=3, max_age_seconds=0.01, auto_refresh=False)
    d['a'] = 'x'
    eq_(d.get('a'), 'x')
    sleep(0.005)
    d['a']
    sleep(0.005)
    eq_(d.get('a'), None)
    sleep(0.01)
    eq_(d.get('a'), None)

def test_auto_expired():
    d = ExpiringDict(max_len=3, max_age_seconds=0.1, auto_expired=True)
    d['a'] = 'x'
    d['b'] = 'y'
    sleep(1)
    ok_('a' not in d._safe_keys())
    ok_('b' not in d._safe_keys())
    eq_(d.get('a'), None)
    eq_(d.get('b'), None)


def test_pop():
    d = ExpiringDict(max_len=3, max_age_seconds=0.01)
    d['a'] = 'x'
    eq_('x', d.pop('a'))
    sleep(0.01)
    eq_(None, d.pop('a'))


def test_repr():
    d = ExpiringDict(max_len=2, max_age_seconds=0.01)
    d['a'] = 'x'
    eq_(str(d), "ExpiringDict([('a', 'x')])")
    sleep(0.01)
    eq_(str(d), "ExpiringDict([])")


def test_iter():
    d = ExpiringDict(max_len=10, max_age_seconds=0.01)
    eq_([k for k in d], [])
    d['a'] = 'x'
    d['b'] = 'y'
    d['c'] = 'z'
    eq_([k for k in d], ['a', 'b', 'c'])

    eq_([k for k in d.values()], ['x', 'y', 'z'])
    sleep(0.01)
    eq_([k for k in d.values()], [])


def test_clear():
    d = ExpiringDict(max_len=10, max_age_seconds=10)
    d['a'] = 'x'
    eq_(len(d), 1)
    d.clear()
    eq_(len(d), 0)


def test_ttl():
    d = ExpiringDict(max_len=10, max_age_seconds=10)
    d['a'] = 'x'

    # existent non-expired key
    ok_(0 < d.ttl('a') < 10)

    # non-existent key
    eq_(None, d.ttl('b'))

    # expired key
    with patch.object(ExpiringDict, '__getitem__',
                      Mock(return_value=('x', 10**9))):
        eq_(None, d.ttl('a'))


def test_setdefault():
    d = ExpiringDict(max_len=10, max_age_seconds=0.01)

    eq_('x', d.setdefault('a', 'x'))
    eq_('x', d.setdefault('a', 'y'))

    sleep(0.01)

    eq_('y', d.setdefault('a', 'y'))


def test_not_implemented():
    d = ExpiringDict(max_len=10, max_age_seconds=10)
    assert_raises(NotImplementedError, d.fromkeys)
    assert_raises(NotImplementedError, d.viewitems)
    assert_raises(NotImplementedError, d.viewkeys)
    assert_raises(NotImplementedError, d.viewvalues)


def test_reset_of_key_no_trim():
    """Re-setting an existing key should not cause a non-expired key to be dropped"""
    d = ExpiringDict(max_len=2, max_age_seconds=10)
    d["a"] = "A"
    d["b"] = "B"

    d["b"] = "B"

    assert "a" in d
