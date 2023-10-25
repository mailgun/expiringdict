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

### 从PyPi安装 | Install from PyPi

Poetry: `poetry add expiringdict`
PDM: `pdm add expiringdict`
pip: `pip install expiringdict`

### 源代码构建 | Build from source

``` bash
git clone git@github.com:AzideCupric/expiringdict.git
poetry build
```

### 安装测试依赖 | Install test dependencies

[Nose](http://readthedocs.org/docs/nose/en/latest/),
[Mock](http://www.voidspace.org.uk/python/mock/),
[coverage](http://nedbatchelder.com/code/coverage/)

``` bash
pip install -e expiringdict[test]
```

## 测试 | Testing

运行以下命令以运行测试：  
To run tests with coverage:

``` bash
nosetests --with-coverage --cover-package=expiringdict
```

## 使用 | Usage

创建一个容量为100个元素且元素在10秒后过期的字典：  
Create a dictionary with capacity for 100 elements and elements expiring in 10 seconds:

``` py
from expiringdict import ExpiringDict
cache = ExpiringDict(max_len=100, max_age_seconds=10)
```

在字典中放入一个值并获取：
put and get a value there:

``` py
cache["key"] = "value"
cache.get("key")
```

从`dict`或`OrderedDict`复制：  
copy from dict or OrderedDict:

``` py
from expiringdict import ExpiringDict
my_dict=dict()
my_dict['test'] = 1
cache = ExpiringDict(max_len=100, max_age_seconds=10, items=my_dict)
assert cache['test'] == 1
```

从另一个ExpiringDict复制，可选新的长度和超时：  
copy from another ExpiringDict, with or without new length and timeout:

``` py
from expiringdict import ExpiringDict
cache_hour = ExpiringDict(max_len=100, max_age_seconds=3600)
cache_hour['test'] = 1
cache_hour_copy = ExpiringDict(max_len=None, max_age_seconds=None, items=cache_hour)
cache_minute_copy = ExpiringDict(max_len=None, max_age_seconds=60, items=cache_hour)
assert cache_minute_copy['test'] == 1
```

从pickle复制：  
pickle:

``` py
import dill
from expiringdict import ExpiringDict
cache = ExpiringDict(max_len=100, max_age_seconds=10)
cache['test'] = 1
pickled_cache = dill.dumps(cache)
unpickled_cache = dill.loads(cache)
assert unpickled_cache['test'] == 1
```

## 鸣谢 | Thanks

本项目是基于 [expiringdict](https://github.com/mailgun/expiringdict) 的修改版。  
This project is a modified version of [expiringdict](https://github.com/mailgun/expiringdict)

缘由是原项目已经很久没有更新，并且缺少好用的类型注解，因此我决定自己维护一份。
