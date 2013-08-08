expiringdict
------------

expiringdict is a Python caching library. The core of the library is ExpiringDict class which is basically an ordered
dictionary with auto-expiring values for caching purposes. Expiration happens on any access, object is locked during
cleanup from expired values. ExpiringDict can not store more than `max_len elements` - the oldest will be deleted.

**NOTE:** iteration over dict and also keys() do not remove expired values!


Installation
------------

Download the sources and run installation command from expiringdict directory:
```
python setup.py install
```
or to install with test dependencies ([Nose](http://readthedocs.org/docs/nose/en/latest/),
[Mock](http://www.voidspace.org.uk/python/mock/) and [coverage](http://nedbatchelder.com/code/coverage/))
run from the directory above:
```
pip install -e expiringdict[test]
```

To run tests with coverage:
```
nosetests --with-coverage --cover-package=expiringdict
```

Usage
-----

Create a dictionary with capacity for 100 elements and elements expiring in 10 seconds:
```python
from expiringdict import ExpiringDict


cache = ExpiringDict(max_len=100, max_age_seconds=10)
```
put and get a value there:
```python
cache["key"] = "value"
cache.get("key")
```
