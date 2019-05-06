from collections import Sequence, Mapping


class YamlDict(dict):

    def __init__(self, *args, **kwargs):
        super(YamlDict, self).__init__(*args, **kwargs)
        self._root = self

    def __repr__(self):
        tmp = self._root
        self._root = None
        res = super(YamlDict, self).__repr__()
        self._root = tmp
        return res

    def __getattr__(self, key):
        if key in self:
            return self[key]
        return super(YamlDict, self).__getattribute__(key)

    def __getitem__(self, key):
        v = super(YamlDict, self).__getitem__(key)
        if self._root is not None and isinstance(v, str):
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
        super(YamlDict, self).__setitem__(key, value)

    def set_as_root(self, root=None):
        if root is None:
            root = self
        self._root = root
        for k, v in self.items():
            if hasattr(v, 'set_as_root'):
                v.set_as_root(root)


class YamlList(list):
    ROOT_NAME = 'root'

    def __init__(self, *args, **kwargs):
        super(YamlList, self).__init__(*args, **kwargs)
        self.__root = {YamlList.ROOT_NAME: self}

    def __getitem__(self, key):
        v = super(YamlList, self).__getitem__(key)
        if isinstance(v, str):
            v = v.format(**self.__root)
        return v

    def __setitem__(self, key, value):
        if isinstance(value, Mapping) and not isinstance(value, YamlDict):
            value = YamlDict(value)
        elif isinstance(value, Sequence) and not isinstance(value, YamlList):
            value = YamlList(value)
        super(YamlList, self).__setitem__(key, value)

    def set_as_root(self, root=None):
        if root is None:
            root = {YamlList.ROOT_NAME: self}
        self.__root = root
        for v in self:
            if hasattr(v, 'setAsRoot'):
                v.set_as_root(root)
