from nose.tools import eq_

from expiringdict import ExpiringDict
import dill

try:
    from collections import OrderedDict
except ImportError:
    # Python < 2.7
    from ordereddict import OrderedDict


def test_expiring_dict_pickle():
    exp_dict_test = ExpiringDict(max_len=200000, max_age_seconds=1800)
    exp_dict_test['test'] = 1
    pickled_object = dill.dumps(exp_dict_test)
    original_object = dill.loads(pickled_object)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    eq_(1, original_object['test'])


def test_expiring_dict_copy_from_dict():
    dict_test = dict()
    dict_test['test'] = 1
    exp_dict_test = ExpiringDict(max_len=200000, max_age_seconds=1800, items=dict_test)
    eq_(1, exp_dict_test['test'])


def test_expiring_dict_copy_from_expiring_dict_original_timeout_and_length():
    exp_dict_test = ExpiringDict(max_len=200000, max_age_seconds=1800)
    exp_dict_test['test'] = 1
    exp_dict_test2 = ExpiringDict(max_len=None, max_age_seconds=None, items=exp_dict_test)
    eq_(1, exp_dict_test2['test'])
    eq_(200000, exp_dict_test2.max_len)
    eq_(1800, exp_dict_test2.max_age)


def test_expiring_dict_copy_from_expiring_dict_new_timeout_and_length():
    exp_dict_test = ExpiringDict(max_len=200000, max_age_seconds=1800)
    exp_dict_test['test'] = 1
    exp_dict_test2 = ExpiringDict(max_len=100000, max_age_seconds=900, items=exp_dict_test)
    eq_(1, exp_dict_test2['test'])
    eq_(100000, exp_dict_test2.max_len)
    eq_(900, exp_dict_test2.max_age)


def test_shallow_copy_preserves_configuration_values_and_timestamps():
    from mock import patch
    with patch('expiringdict.time.time', return_value=100) as clock:
        cache = ExpiringDict(max_len=3, max_age_seconds=10)
        payload = []
        cache['key'] = payload
        clock.return_value = 105
        copied = cache.copy()
        eq_(type(copied), type(cache))
        eq_(copied.max_len, 3)
        eq_(copied.max_age, 10)
        assert copied['key'] is payload
        eq_(copied.items_with_timestamp(), cache.items_with_timestamp())
        copied['other'] = 'value'
        assert 'other' not in cache
        clock.return_value = 110
        assert 'key' not in copied


def test_shallow_copy_empty_cache():
    cache = ExpiringDict(max_len=3, max_age_seconds=10)
    copied = cache.copy()
    eq_(copied.items(), [])
    eq_(copied.max_len, cache.max_len)
    eq_(copied.max_age, cache.max_age)
