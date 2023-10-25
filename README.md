# Expiring TypedDict

[![image](https://coveralls.io/repos/github/mailgun/expiringdict/badge.svg?branch=master)](https://coveralls.io/github/mailgun/expiringdict?branch=master)

expiringdict是一个Python缓存库。
expiringdict is a Python caching library.

该库的核心是ExpiringDict类，它是一个带有自动过期值的有序字典，用于缓存目的。
The core of the library is ExpiringDict class which is an ordered dictionary with auto-expiringvalues for caching purposes.

在任何访问时都会发生过期，对象在清理过期值期间被锁定。
Expiration happens on any access, object is locked during cleanup from expired values.

ExpiringDict不能存储超过`max_len`个元素 - 最旧的元素将被删除。
ExpiringDict can not store more than `max_len` elements - the oldest will be deleted.

> [!NOTE]
> 对字典进行迭代以及使用keys()方法不会删除过期的值！
> Iteration over dict and also keys() do not remove expired values!

## 安装 | Installation

If you wish to install from PyPi:

``` bash
pip install expiringdict
```

If you wish to download the source and install from GitHub:

``` bash
git clone git@github.com:mailgun/expiringdict.git
python setup.py install
```

or to install with test dependencies
([Nose](http://readthedocs.org/docs/nose/en/latest/),
[Mock](http://www.voidspace.org.uk/python/mock/),
[coverage](http://nedbatchelder.com/code/coverage/)) run from the
directory above:

``` bash
pip install -e expiringdict[test]
```

To run tests with coverage:

``` bash
nosetests --with-coverage --cover-package=expiringdict
```

## Usage

Create a dictionary with capacity for 100 elements and elements expiring
in 10 seconds:

``` py
from expiringdict import ExpiringDict
cache = ExpiringDict(max_len=100, max_age_seconds=10)
```

put and get a value there:

``` py
cache["key"] = "value"
cache.get("key")
```

copy from dict or OrderedDict:

``` py
from expiringdict import ExpiringDict
my_dict=dict()
my_dict['test'] = 1
cache = ExpiringDict(max_len=100, max_age_seconds=10, items=my_dict)
assert cache['test'] == 1
```

copy from another ExpiringDict, with or without new length and timeout:

``` py
from expiringdict import ExpiringDict
cache_hour = ExpiringDict(max_len=100, max_age_seconds=3600)
cache_hour['test'] = 1
cache_hour_copy = ExpiringDict(max_len=None, max_age_seconds=None, items=cache_hour)
cache_minute_copy = ExpiringDict(max_len=None, max_age_seconds=60, items=cache_hour)
assert cache_minute_copy['test'] == 1
```

pickle :

``` py
import dill
from expiringdict import ExpiringDict
cache = ExpiringDict(max_len=100, max_age_seconds=10)
cache['test'] = 1
pickled_cache = dill.dumps(cache)
unpickled_cache = dill.loads(cache)
assert unpickled_cache['test'] == 1
```
