from time import sleep

from mock import Mock, patch

from expiringdict import ExpiringDict

from pytest import raises


def test_create():
    with raises(AssertionError):
        ExpiringDict(max_len=1, max_age_seconds=-1)
        ExpiringDict(max_len=0, max_age_seconds=1)

    d = ExpiringDict(max_len=3, max_age_seconds=0.01)
    assert len(d) == 0


def test_basics():
    d = ExpiringDict(max_len=3, max_age_seconds=0.01)

    assert d.get('a') is None
    d['a'] = 'x'
    assert d.get('a') == 'x'

    sleep(0.01)
    assert d.get('a') is None

    d['a'] = 'y'
    assert d.get('a') == 'y'

    assert 'b' not in d
    d['b'] = 'y'
    assert 'b' in d

    sleep(0.01)
    assert 'b' not in d

    # a is still in expiringdict, next values should expire it
    d['c'] = 'x'
    d['d'] = 'y'
    d['e'] = 'z'

    # dict if full
    assert 'c' in d
    assert 'd' in d

    d['f'] = '1'
    # c should gone after that
    assert 'c' not in d, 'Len of dict is more than max_len'

    # test __delitem__
    del d['e']
    assert 'e' not in d


def test_pop():
    d = ExpiringDict(max_len=3, max_age_seconds=0.01)
    d['a'] = 'x'
    assert 'x' == d.pop('a')
    sleep(0.01)
    assert d.pop('a') is None


def test_repr():
    d = ExpiringDict(max_len=2, max_age_seconds=0.01)
    d['a'] = 'x'
    assert str(d) == "ExpiringDict([('a', 'x')])"
    sleep(0.01)
    assert str(d) == "ExpiringDict([])"


def test_iter():
    d = ExpiringDict(max_len=10, max_age_seconds=0.01)
    assert [k for k in d] == []
    d['a'] = 'x'
    d['b'] = 'y'
    d['c'] = 'z'
    assert [k for k in d] == ['a', 'b', 'c']

    assert [k for k in d.values()] == ['x', 'y', 'z']
    sleep(0.01)
    assert [k for k in d.values()] == []


def test_clear():
    d = ExpiringDict(max_len=10, max_age_seconds=10)
    d['a'] = 'x'
    assert len(d) == 1
    d.clear()
    assert len(d) == 0


def test_ttl():
    d = ExpiringDict(max_len=10, max_age_seconds=10)
    d['a'] = 'x'

    # existent non-expired key
    assert 0 < d.ttl('a') < 10

    # non-existent key
    assert d.ttl('b') is None

    # expired key
    with patch.object(ExpiringDict, '__getitem__',
                      Mock(return_value=('x', 10**9))):
        assert d.ttl('a') is None


def test_setdefault():
    d = ExpiringDict(max_len=10, max_age_seconds=0.01)

    assert d.setdefault('a', 'x') == 'x'
    assert d.setdefault('a', 'y') == 'x'

    sleep(0.01)

    assert d.setdefault('a', 'y') == 'y'


def test_not_implemented():
    d = ExpiringDict(max_len=10, max_age_seconds=10)
    with raises(NotImplementedError):
        d.fromkeys()
        d.viewitems()
        d.viewkeys()
        d.viewvalues()


def test_reset_of_key_no_trim():
    """Re-setting an existing key should not cause a non-expired key to be dropped"""
    d = ExpiringDict(max_len=2, max_age_seconds=10)
    d["a"] = "A"
    d["b"] = "B"

    d["b"] = "B"

    assert "a" in d
