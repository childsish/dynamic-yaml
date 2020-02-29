from collections import Sequence, Mapping


class YamlDict(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._root = self

    def __getattr__(self, key):
        if key in self:
            return self[key]
        return super().__getattribute__(key)

    def __getitem__(self, key):
        v = super().__getitem__(key)
        if isinstance(v, str):
            v = v.format(**self._root)
        return v

    def __setitem__(self, key, value):
        if isinstance(value, Mapping) and not isinstance(value, YamlDict):
            value = YamlDict(value)
            value.set_as_root(self._root)
        elif isinstance(value, str):
            pass
        elif isinstance(value, Sequence) and not isinstance(value, YamlList):
            value = YamlList(value)
        super().__setitem__(key, value)

    def set_as_root(self, root=None):
        if root is not None:
            self._root = root
        for k, v in self.items():
            if hasattr(v, 'set_as_root'):
                v.set_as_root(self._root)


class YamlList(list):
    ROOT_NAME = 'root'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._root = {YamlList.ROOT_NAME: self}

    def __getitem__(self, key):
        v = super().__getitem__(key)
        if isinstance(v, str):
            v = v.format(**self._root)
        return v

    def __setitem__(self, key, value):
        if isinstance(value, Mapping) and not isinstance(value, YamlDict):
            value = YamlDict(value)
        elif isinstance(value, str):
            pass
        elif isinstance(value, Sequence) and not isinstance(value, YamlList):
            value = YamlList(value)
        super().__setitem__(key, value)

    def set_as_root(self, root=None):
        if root is not None:
            self._root = root
        for v in self:
            if hasattr(v, 'set_as_root'):
                v.set_as_root(self._root)
