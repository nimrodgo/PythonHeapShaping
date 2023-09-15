import heapq
import functools
from typing import Any

@functools.total_ordering
class DictItem:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __lt__(self, other):
        return self.key < other.key

    def __eq__(self, other):
        return self.key == other.key

    def __iter__(self):
        yield self.key
        yield self.value
    
    def __repr__(self):
        return f'DictItem({self.key}, {self.value})'


class HeapDict:
    def __init__(self, items=None):
        self._items = items if items else []
        heapq.heapify(self._items)

    def __setitem__(self, key, value):
        heapq.heappush(self._items, DictItem(key, value))

    def __getitem__(self, key):
        return self._items[self._items.index(DictItem(key, None))].value

    def items(self):
        return iter(self._items)

    def __iter__(self):
        for key, _ in self._items:
            yield key

    def __repr__(self):
        return f'HeapDict({self._items})'

class Compound:
    def __init__(self, data, *, parent=None, filter=lambda _: None):
        self._underlying_dict = HeapDict()
        self._parent = parent
        self._filter = filter
        for key in data:
            self._underlying_dict[key] = self._as_item(data[key])
        self.init = True

    def __setattr__(self, name, value):
        if 'init' in self.__dict__:
            self.merge_to(name, value)
        else:
            self.__dict__[name] = value

    def ancestor(self):
        result = self
        while result._parent:
            result = result._parent
        return result

    def __getattr__(self, name):
        '''
        Simplify pathing, so a.b in config will lead to the right place
        '''
        if not name:
            return self


        splitted = name.rsplit('.', 1)
        parent = self if len(splitted) == 1 else getattr(self, splitted[0])
        name = splitted[-1]

        if name not in parent._underlying_dict:
            parent._underlying_dict[name] = Compound({}, parent=parent, filter=parent._filter)

        item = parent._underlying_dict[name]

        if isinstance(item, str) and item[0] == '$':
            item = getattr(self.ancestor(), item[1:])

        return item

    def merge_to(self, path, other):
        '''
        merges two entries, returns whether the result was changed
        '''
        parent = getattr(self, path)
        for key, value in other._underlying_dict.items():
            self._filter(key)
            parent._underlying_dict[key] = parent._as_item(value)

    def _as_item(self, new_value):
        if isinstance(new_value, Compound):
            return Compound(new_value._underlying_dict, parent=self, filter=self._filter)
        if isinstance(new_value, dict):
            return Compound(new_value, parent=self, filter=self._filter)
        if isinstance(new_value, list):
            return [self._as_item(item) for item in new_value]
        return new_value

    @staticmethod
    def load_from_dict(json_object, filter=lambda _: None):
        result = Compound({}, filter=filter)
        for key, value in json_object.items():
            result._underlying_dict[key] = result._as_item(value)
        return result
