from expiringdict import ExpiringDict
import dill

try:
    from collections import OrderedDict
except ImportError:
    # Python < 2.7
    from ordereddict import OrderedDict


def test_expiring_dict_pickle():
    """
    >>> test_expiring_dict_pickle()
    """

    exp_dict_test = ExpiringDict(max_len=200000, max_age_seconds=1800)
    exp_dict_test['test'] = 1
    pickled_object = dill.dumps(exp_dict_test)
    original_object = dill.loads(pickled_object)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    result = original_object['test']
    assert result == 1


def test_expiring_dict_copy_from_dict():
    """
    >>> test_expiring_dict_copy_from_dict()
    """
    dict_test = dict()
    dict_test['test'] = 1
    exp_dict_test = ExpiringDict(max_len=200000, max_age_seconds=1800, items=dict_test)
    result = exp_dict_test['test']
    assert result == 1


def test_expiring_dict_copy_from_expiring_dict_original_timeout_and_length():
    """
    >>> test_expiring_dict_copy_from_expiring_dict_original_timeout_and_length()
    """

    exp_dict_test = ExpiringDict(max_len=200000, max_age_seconds=1800)
    exp_dict_test['test'] = 1
    exp_dict_test2 = ExpiringDict(max_len=None, max_age_seconds=None, items=exp_dict_test)
    result = exp_dict_test2['test'], exp_dict_test2.max_len, exp_dict_test2.max_age
    assert result == (1, 200000, 1800)


def test_expiring_dict_copy_from_expiring_dict_new_timeout_and_length():
    """
    >>> test_expiring_dict_copy_from_expiring_dict_new_timeout_and_length()
    """

    exp_dict_test = ExpiringDict(max_len=200000, max_age_seconds=1800)
    exp_dict_test['test'] = 1
    exp_dict_test2 = ExpiringDict(max_len=100000, max_age_seconds=900, items=exp_dict_test)
    result = exp_dict_test2['test'], exp_dict_test2.max_len, exp_dict_test2.max_age
    assert result == (1, 100000, 900)
