expiringdict
============

Introduction
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

License
-------

(The MIT License)

Copyright (c) 2012, 2013, 2014, 2015

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
