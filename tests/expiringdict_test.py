from . import *
from expiringdict import *
from time import sleep


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

def test_eviction_on_wrong_count():
    d = ExpiringDict(max_len=3, max_age_seconds=20)
    d['a'] = 'x'
    d['b'] = 'y'
    d['c'] = 'z'
    d['b'] = 'y'
    eq_([k for k in d], ['a', 'b', 'c'])
    eq_([k for k in d.values()], ['x', 'y', 'z'])

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


def test_eviction_counting():
    d = ExpiringDict(max_len=1, max_age_seconds=100, eviction_counter=0)

    d['a'] = 'A'
    d['b'] = 'B'
    d['c'] = 'C'

    eq_(len(d), 1)
    eq_(d.evictions, 2)


def test_eviction_reset():
    d = ExpiringDict(max_len=1, max_age_seconds=100, eviction_counter=0)

    d['a'] = 'A'
    d['b'] = 'B'
    d['c'] = 'C'

    current_eviction_count = d.reset_evictions()
    eq_(len(d), 1)
    eq_(current_eviction_count, 2)
    eq_(d.evictions, 0)
    check_eviction_count = d.reset_evictions(1) # anything that supports +=
    d['d'] = 'D'
    eq_(len(d), 1)
    eq_(check_eviction_count, 0) # no operations before reset
    eq_(d.evictions, 2)  # since we started at 1


def test_not_implemented():
    d = ExpiringDict(max_len=10, max_age_seconds=10)
    assert_raises(NotImplementedError, d.fromkeys)
    assert_raises(NotImplementedError, d.iteritems)
    assert_raises(NotImplementedError, d.itervalues)
    assert_raises(NotImplementedError, d.viewitems)
    assert_raises(NotImplementedError, d.viewkeys)
    assert_raises(NotImplementedError, d.viewvalues)
