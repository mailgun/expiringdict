from collections import OrderedDict
from mock import Mock, patch
from nose.tools import ok_, eq_, assert_raises
from expiringdict import ExpiringDict
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
    with patch.object(OrderedDict, '__getitem__',
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


def test_update_at_the_top_capacity():
    """
    Reveals a bug where an update of an existing key when a dictionary has
    maxed out its capacity resulting in a loss of the least recently added
    element.
    """
    # Given
    d = ExpiringDict(max_len=3, max_age_seconds=10)
    d['a'] = 1
    d['b'] = 2
    d['c'] = 3
    # When
    d['b'] = 4
    # Then: key `a` is still in the dictionary.
    eq_({'a': 1, 'b': 4, 'c': 3}, d.to_dict())


def test_lru_behavior_on_write():
    """
    If a new element is added to the dictionary that has reached the maximum of
    its capacity then the least recently used element is thrown away to give
    space to the new element.

    In particular it checks that value update is qualified as usage.
    """
    # Given
    d = ExpiringDict(max_len=2, max_age_seconds=10)
    d['a'] = 1
    d['b'] = 2
    # When
    d['a'] = 3
    d['c'] = 4
    # Then: Least recently used key `b` has been cast away.
    eq_({'a': 3, 'c': 4}, d.to_dict())


def test_lru_behavior_on_read():
    """
    If a new element is added to the dictionary that has reached the maximum of
    its capacity then the least recently used element is thrown away to give
    space to the new element.

    In particular it checks that value reading is qualified as usage.
    """
    # Given
    d = ExpiringDict(max_len=2, max_age_seconds=10)
    d['a'] = 1
    d['b'] = 2
    # When
    print(d['a'])
    d['c'] = 4
    # Then: Least recently used key `b` has been cast away.
    eq_({'a': 1, 'c': 4}, d.to_dict())
