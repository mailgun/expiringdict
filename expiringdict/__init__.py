from threading import RLock
from datetime import datetime
from types import MappingProxyType
from collections.abc import Mapping
from typing import Generic, TypeVar

KT = TypeVar("KT")
VT = TypeVar("VT")


class ExpiringDict(Generic[KT, VT]):
    def __init__(self, max_len: int, max_age_seconds: float, items: Mapping[KT, VT] | None = None):
        if max_len < 1:
            raise ValueError("max_len must be >= 1")
        if max_age_seconds < 0:
            raise ValueError("max_age_seconds must be >= 0")

        self.max_len = max_len
        self.max_age = max_age_seconds
        self.lock = RLock()
        self._dict: dict[KT, tuple[VT, datetime]] = {}
        if items is not None:
            self._build_from_mapping(items)

    def __len__(self):
        """Return the number of items in the dictionary."""
        with self.lock:
            return len([value for key, value in self._dict.items() if key in self])

    def __delitem__(self, key: KT):
        with self.lock:
            del self._dict[key]

    def _build_from_mapping(self, items: Mapping[KT, VT]):
        for key, value in items.items():
            self.__setitem__(key, value)

    def _is_died(self, item: tuple[VT, datetime]):
        item_age = datetime.now() - item[1]
        if item_age.seconds > self.max_age:
            return True
        return False

    def __contains__(self, key: KT):
        """Return True if the dict has a key, else return False."""
        try:
            with self.lock:
                item = self._dict[key]
                if self._is_died(item):
                    del self[key]
                    return False
                return True
        except KeyError:
            return False

    def __getitem__(self, key: KT):
        """Return the item of the dict.

        Raises a KeyError if key is not in the map.
        """
        with self.lock:
            item = self._dict[key]
            if self._is_died(item):
                del self[key]
                raise KeyError(key)
            return item[0]

    def __setitem__(self, key: KT, value: VT, set_time: datetime | None = None):
        """Set d[key] to value.

        If the dictionary has no room, remove the least recently used item.
        """
        if not self.max_len:
            return

        with self.lock:
            length = len(self)
            if length == self.max_len and length:
                if key in self:
                    del self[key]
                else:
                    self.popitem()

            self._dict[key] = (value, set_time or datetime.now())

    def pop(self, key: KT, default: VT | None = None):
        """Get item from the dict and remove it.

        Return default if expired or does not exist. Never raise KeyError.
        """
        with self.lock:
            try:
                value, _ = self._dict.pop(key)
                return value
            except KeyError:
                return default

    def popitem(self):
        """Get and remove the (key, value) pair least recently used."""
        with self.lock:
            return self._dict.popitem()

    def ttl(self, key: KT):
        """Return TTL of the `key` (in seconds).

        Returns None for non-existent or expired keys.
        """
        _, key_age = self.get_with_age(key)
        if key_age:
            key_ttl = self.max_age - key_age
            if key_ttl > 0:
                return key_ttl
        return None

    def get(self, key: KT, default: VT | None = None):
        """Return the value for key if key is in the dictionary, else default."""
        try:
            item = self._dict[key]
            if self._is_died(item):
                del self[key]
                return default
            return item[0]
        except KeyError:
            return default

    def get_with_age(self, key: KT, default: VT | None = None):
        """Return the value for key if key is in the dictionary, else default."""
        item = self._dict[key]
        if self._is_died(item):
            del self[key]
            return default, None

        return item[0], (datetime.now() - item[1]).seconds

    def items(self):
        """Return a copy of the dictionary's list of (key, value) pairs."""
        return [(key, value[0]) for key, value in self._dict.items() if key in self]

    def items_with_datetime(self):
        """Return a copy of the dictionary's list of (key, value, datetime) triples."""
        return [(key, value[0], value[1]) for key, value in self._dict.items() if key in self]

    def values(self):
        """Return a copy of the dictionary's list of values.
        See the note for dict.items()."""
        return [value[0] for key, value in self._dict.items() if key in self]

    def fromkeys(self, keys: list[KT], value: VT, time: datetime | None = None):
        """Create a new dictionary with keys from seq and values set to value."""
        for key in keys:
            self.__setitem__(key, value, time)
        return self

    def iteritems(self):
        """Return an iterator over the dictionary's (key, value) pairs."""
        return ((key, value[0]) for key, value in self._dict.items() if key in self)

    def itervalues(self):
        """Return an iterator over the dictionary's values."""
        return (value[0] for key, value in self._dict.items() if key in self)

    def viewitems(self):
        """Return a new view of the dictionary's items ((key, value) pairs)."""
        return MappingProxyType({key: value[0] for key, value in self._dict.items() if key in self})

    def viewkeys(self):
        """Return a new view of the dictionary's keys."""
        return MappingProxyType({key: value[0] for key, value in self._dict.items() if key in self}).keys()

    def viewvalues(self):
        """Return a new view of the dictionary's values."""
        return MappingProxyType({key: value[0] for key, value in self._dict.items() if key in self}).values()

    def __reduce__(self):
        return self.__class__, (self.max_len, self.max_age, self.items_with_datetime())
