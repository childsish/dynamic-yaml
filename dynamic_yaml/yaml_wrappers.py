import re

from collections.abc import Collection, Mapping, MutableMapping, MutableSequence, Sequence


class DynamicYamlObject(Collection):
    def __init__(self):
        super().__setattr__('_collection', {})
        super().__setattr__('_root', {})
        super().__setattr__('_recursive', False)
        super().__setattr__('_regx', re.compile('.*{.*}.*', re.DOTALL))

    def __iter__(self):
        yield from super().__getattribute__('_collection')

    def __contains__(self, value: object) -> bool:
        return value in super().__getattribute__('_collection')

    def __len__(self) -> int:
        return len(super().__getattribute__('_collection'))

    def __getitem__(self, key):
        value = super().__getattribute__('_collection')[key]
        if isinstance(value, str):
            while super().__getattribute__('_regx').match(value) is not None:
                value = value.format(**super().__getattribute__('_root')._collection)
                if not super().__getattribute__('_recursive'):
                    break
        return value

    def __setitem__(self, key, value):
        if isinstance(value, Mapping) and not isinstance(value, YamlDict):
            value = YamlDict(value)
            value._set_as_root(super().__getattribute__('_root'))
        elif isinstance(value, Sequence) and not isinstance(value, (str, YamlList)):
            value = YamlList(value)
            value._set_as_root(super().__getattribute__('_root'))
        super().__getattribute__('_collection')[key] = value

    def __delitem__(self, key):
        del super().__getattribute__('_collection')[key]

    def _values(self):
        raise NotImplementedError('This method must be implemented in the child class')

    def _set_as_root(self, root=None, *, recursive=False):
        super().__setattr__('_recursive', recursive)
        if root is not None:
            super().__setattr__('_root', root)
        for value in self._values():
            if isinstance(value, DynamicYamlObject):
                value._set_as_root(super().__getattribute__('_root'), recursive=recursive)


class YamlDict(DynamicYamlObject, MutableMapping):
    def __init__(self, *args, **kwargs):
        super().__init__()
        super().__setattr__('_collection', dict(*args, **kwargs))
        super().__setattr__('_root', self)

    def __getattr__(self, key):
        if key in self:
            return self[key]
        return super().__getattribute__(key)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        del self[key]

    def _values(self):
        return super().__getattribute__('_collection').values()


class YamlList(DynamicYamlObject, MutableSequence):
    ROOT_NAME = 'root'

    def __init__(self, *args, **kwargs):
        super().__init__()
        super().__setattr__('_collection', list(*args, **kwargs))
        super().__setattr__('_root', YamlDict([(YamlList.ROOT_NAME, self)]))

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def insert(self, index: int, object):
        super().__getattribute__('_collection').insert(index, object)

    def _values(self):
        return super().__getattribute__('_collection')
