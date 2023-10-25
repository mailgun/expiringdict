from time import sleep
from datetime import timedelta

import pytest
from expiringdict import ExpiringDict, ExpiringDictCreateError


def test_create():
    with pytest.raises(ExpiringDictCreateError):
        ExpiringDict(max_len=1, max_age_seconds=-1)

    with pytest.raises(ExpiringDictCreateError):
        ExpiringDict(max_len=0, max_age_seconds=1)

    d: ExpiringDict[str, int] = ExpiringDict(max_len=3, max_age_seconds=0.01)
    assert len(d) == 0


def test_basics():
    d: ExpiringDict[str, str] = ExpiringDict(max_len=3, max_age_seconds=0.01)

    assert d.get("a") is None
    d["a"] = "x"
    assert d.get("a") == "x"

    sleep(0.01)
    assert d.get("a") is None

    d["a"] = "y"
    assert d.get("a") == "y"

    assert "b" not in d
    d["b"] = "y"
    assert "b" in d

    sleep(0.01)
    assert "b" not in d

    # a is still in expiringdict, next values should expire it
    d["c"] = "x"
    d["d"] = "y"
    d["e"] = "z"

    # dict if full
    assert "c" in d
    assert "d" in d
    d["f"] = "1"

    # c should gone after that
    assert "e" not in d

    # test __delitem__
    del d["c"]
    assert "c" not in d


def test_pop():
    d = ExpiringDict(max_len=3, max_age_seconds=0.01)
    d["a"] = "x"
    assert "x" == d.pop("a")
    sleep(0.01)
    assert None is d.pop("a")


def test_repr():
    d = ExpiringDict(max_len=2, max_age_seconds=0.01)
    d["a"] = "x"
    assert str(d) == "ExpiringDict([('a', 'x')])"
    sleep(0.01)
    assert str(d) == "ExpiringDict([])"


def test_iter():
    d: ExpiringDict[str, str] = ExpiringDict(max_len=10, max_age_seconds=0.01)
    assert len(d) == 0
    d["a"] = "x"
    d["b"] = "y"
    d["c"] = "z"
    assert list(d) == ["a", "b", "c"]

    assert d.values() == ["x", "y", "z"]
    sleep(0.01)
    assert list(d.values()) == []


def test_clear():
    d = ExpiringDict(max_len=10, max_age_seconds=10)
    d["a"] = "x"
    assert len(d) == 1
    d.clear()
    assert len(d) == 0


def test_ttl():
    d = ExpiringDict(max_len=10, max_age_seconds=10)
    d["a"] = "x"

    sleep(1)
    # existent non-expired key
    assert 0 < (d.ttl("a") or timedelta(seconds=0)).seconds < 10

    # non-existent key
    assert None is d.ttl("b")

    # expired key
    sleep(10)
    assert None is d.ttl("a")


def test_reset_of_key_no_trim():
    """Re-setting an existing key should not cause a non-expired key to be dropped"""
    d = ExpiringDict(max_len=2, max_age_seconds=10)
    d["a"] = "A"
    d["b"] = "B"

    d["b"] = "B"

    assert "a" in d
