import re

from collections import Sequence, Mapping


class YamlDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().__setattr__('_root', self)
        super().__setattr__('_recursive', False)
        super().__setattr__('_regx', re.compile('.*{.*}.*'))

    def __getattr__(self, key):
        if key in self:
            return self[key]
        return super().__getattribute__(key)

    def __setattr__(self, key, value):
        self[key] = value

    def __getitem__(self, key):
        v = super().__getitem__(key)
        if isinstance(v, str):
            while self._regx.match(v) is not None:
                v = v.format(**super().__getattribute__('_root'))
                if not self._recursive:
                    break
        return v

    def __setitem__(self, key, value):
        if isinstance(value, Mapping) and not isinstance(value, YamlDict):
            value = YamlDict(value)
            value.set_as_root(super().__getattribute__('_root'))
        elif isinstance(value, Sequence) and not isinstance(value, (str, YamlList)):
            value = YamlList(value)
            value.set_as_root(super().__getattribute__('_root'))
        super().__setitem__(key, value)

    def set_as_root(self, root=None, *, recursive=False):
        super().__setattr__('_recursive', recursive)
        if root is not None:
            super().__setattr__('_root', root)
        for k, v in self.items():
            if hasattr(v, 'set_as_root'):
                v.set_as_root(super().__getattribute__('_root'), recursive=recursive)


class YamlList(list):
    ROOT_NAME = 'root'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().__setattr__('_root', {YamlList.ROOT_NAME: self})
        super().__setattr__('_recursive', False)
        super().__setattr__('_regx', re.compile('.*{.*}.*'))

    def __getitem__(self, key):
        v = super().__getitem__(key)
        if isinstance(v, str):
            while self._regx.match(v) is not None:
                v = v.format(**super().__getattribute__('_root'))
                if not self._recursive:
                    break
        return v

    def __setitem__(self, key, value):
        if isinstance(value, Mapping) and not isinstance(value, YamlDict):
            value = YamlDict(value)
            value.set_as_root(super().__getattribute__('_root'))
        elif isinstance(value, Sequence) and not isinstance(value, (str, YamlList)):
            value = YamlList(value)
            value.set_as_root(super().__getattribute__('_root'))
        super().__setitem__(key, value)

    def set_as_root(self, root=None, *, recursive=False):
        super().__setattr__('_recursive', recursive)
        if root is not None:
            super().__setattr__('_root', root)
        for v in self:
            if hasattr(v, 'set_as_root'):
                v.set_as_root(super().__getattribute__('_root'), recursive=recursive)
