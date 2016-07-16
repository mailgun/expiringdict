from . import *
from expiringdict import *
from time import sleep


def test_create():
    assert_raises(AssertionError, ExpiringDict, max_len=1, max_age_seconds=-1)
    assert_raises(AssertionError, ExpiringDict, max_len=0, max_age_seconds=1)

    d = ExpiringDict(max_len=3, max_age_seconds=0.01)
    eq_(len(d), 0)


def test_setgetitem():
    d = ExpiringDict(max_len=3, max_age_seconds=0.01)

    d['a'] = 'x'
    eq_(d['a'], 'x')


def test_get_method_unset_item():
    d = ExpiringDict(max_len=3, max_age_seconds=0.01)

    eq_(d.get('a'), None)


def test_max_age_expires():
    d = ExpiringDict(max_len=3, max_age_seconds=0.01)

    d['a'] = 'x'
    sleep(0.01)
    eq_(d.get('a'), None)


def test_update_existing_item():
    d = ExpiringDict(max_len=3, max_age_seconds=0.01)

    d['a'] = 'x'
    eq_(d.get('a'), 'x')

    d['a'] = 'y'
    eq_(d.get('a'), 'y')


def test_key_in():
    d = ExpiringDict(max_len=3, max_age_seconds=0.01)

    d['b'] = 'y'
    ok_('b' in d)


def test_key_not_in():
    d = ExpiringDict(max_len=3, max_age_seconds=0.01)

    ok_('b' not in d)


def test_max_items_expires():
    d = ExpiringDict(max_len=3, max_age_seconds=0.01)

    d['a'] = 1
    d['b'] = 2
    d['c'] = 3
    # a is still in expiringdict, next value should expire it
    d['d'] = 4

    # dict if full
    eq_(len(d), 3)
    ok_('a' not in d)
    ok_('b' in d)
    ok_('c' in d)
    ok_('d' in d)


def test_delitem():
    d = ExpiringDict(max_len=3, max_age_seconds=0.01)

    d['e'] = 1
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


def test_iter():
    d = ExpiringDict(max_len=10, max_age_seconds=0.01)
    eq_([k for k in d], [])
    d['a'] = 'x'
    d['b'] = 'y'
    d['c'] = 'z'
    eq_([k for k in d], ['a', 'b', 'c'])

    eq_([k for k in d.values()], ['x', 'y', 'z'])
    sleep(0.01)
    # eq_(list(d.values()), [])
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
    assert_raises(NotImplementedError, d.iteritems)
    assert_raises(NotImplementedError, d.itervalues)
    assert_raises(NotImplementedError, d.viewitems)
    assert_raises(NotImplementedError, d.viewkeys)
    assert_raises(NotImplementedError, d.viewvalues)
