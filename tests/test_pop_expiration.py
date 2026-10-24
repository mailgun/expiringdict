"""Expiration behavior for pop(), including the exact TTL boundary."""
from collections import OrderedDict

from mock import patch
from nose.tools import eq_, ok_

from expiringdict import ExpiringDict


def test_pop_observes_expiration():
    for age in (0, 9, 10, 11):
        for value in ('cached', None, 0):
            cache = ExpiringDict(4, 10)
            cache.__setitem__('key', value, set_time=100)
            default = object()
            with patch('expiringdict.time.time', return_value=100 + age):
                expected = value if age < 10 else default
                ok_(cache.pop('key', default) is expected)
            ok_(not OrderedDict.__contains__(cache, 'key'))
            ok_(cache.pop('key', default) is default)


def test_pop_default_none_and_live_remaining_entry():
    cache = ExpiringDict(4, 10)
    cache.__setitem__('expired', 'old', set_time=90)
    cache.__setitem__('live', 'new', set_time=99)
    with patch('expiringdict.time.time', return_value=100):
        eq_(cache.pop('expired'), None)
        eq_(cache['live'], 'new')
        eq_(cache.pop('absent'), None)
        eq_(cache.pop('live'), 'new')
