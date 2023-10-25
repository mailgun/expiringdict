from expiringdict import ExpiringDict


def test_expiring_dict_copy_from_dict():
    dict_test: dict[str, int] = {}
    dict_test["test"] = 1
    exp_dict_test = ExpiringDict(max_len=200000, max_age_seconds=1800, items=dict_test)
    assert 1 == exp_dict_test["test"]


def test_expiring_dict_copy_from_expiring_dict_original_timeout_and_length():
    exp_dict_test: ExpiringDict[str, int] = ExpiringDict(max_len=200000, max_age_seconds=1800)
    exp_dict_test["test"] = 1
    exp_dict_test2 = ExpiringDict.fromexdict(exp_dict_test)
    assert 1 == exp_dict_test2["test"]
    assert 200000 == exp_dict_test2.max_len
    assert 1800 == exp_dict_test2.max_age.seconds


def test_expiring_dict_copy_from_expiring_dict_new_timeout_and_length():
    exp_dict_test: ExpiringDict[str, int] = ExpiringDict(max_len=200000, max_age_seconds=1800)
    exp_dict_test["test"] = 1
    exp_dict_test2 = ExpiringDict.fromexdict(exp_dict_test, max_len=100000, max_age_seconds=900)
    assert 1 == exp_dict_test2["test"]
    assert 100000 == exp_dict_test2.max_len
    assert 900 == exp_dict_test2.max_age.seconds
