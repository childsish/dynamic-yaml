import re
import yaml

from collections import OrderedDict, Sequence, Mapping

class YamlDict(OrderedDict):

    def __init__(self, *args, **kwargs):
        super(YamlDict, self).__init__(*args, **kwargs)
        self.__root = self
    
    def __getattr__(self, key):
        if key in self:
            return self[key]
        return super(YamlDict, self).__getattribute__(key)
    
    def __getitem__(self, key):
        v = super(YamlDict, self).__getitem__(key)
        if isinstance(v, basestring):
            v = v.format(**self.__root)
        return v
    
    def __setitem__(self, key, value):
        if isinstance(value, Mapping) and not isinstance(value, YamlDict):
            value = YamlDict(value)
        elif isinstance(value, basestring):
            pass
        elif isinstance(value, Sequence) and not isinstance(value, YamlList):
            value = YamlList(value)
        super(YamlDict, self).__setitem__(key, value)
    
    def setAsRoot(self, root=None):
        if root is None:
            root = self
        self.__root = root
        for k, v in self.iteritems():
            if hasattr(v, 'setAsRoot'):
                v.setAsRoot(root)

class YamlList(list):
    ROOT_NAME = 'root'
    
    def __init__(self, *args, **kwargs):
        super(YamlList, self).__init__(*args, **kwargs)
        self.__root = {YamlList.ROOT_NAME: self}
    
    def __getitem__(self, key):
        v = super(YamlList, self).__getitem__(key)
        if isinstance(v, basestring):
            v = v.format(**self.__root)
        return v
    
    def __setitem__(self, key, value):
        if isinstance(value, Mapping) and not isinstance(value, YamlDict):
            value = YamlDict(value)
        elif isinstance(value, Sequence) and not isinstance(value, YamlList):
            value = YamlList(value)
        super(YamlList, self).__setitem__(key, value)
    
    def setAsRoot(self, root=None):
        if root is None:
            root = {YamlList.ROOT_NAME: self}
        self.__root = root
        for v in self:
            if hasattr(v, 'setAsRoot'):
                v.setAsRoot(root)

def load(infile):
    yaml.add_constructor(u'tag:yaml.org,2002:seq', construct_sequence)
    yaml.add_constructor(u'tag:yaml.org,2002:map', construct_mapping)
    
    infile.seek(0)
    data = yaml.load(infile)
    data.setAsRoot()
    return data

def construct_sequence(loader, node):
    return YamlList(loader.construct_object(child) for child in node.value)

def construct_mapping(loader, node):
    make_obj = loader.construct_object
    return YamlDict((make_obj(k), make_obj(v)) for k, v in node.value)
