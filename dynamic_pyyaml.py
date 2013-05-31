import yaml

from _abcoll import Mapping
from collections import OrderedDict

class YamlDictionary(OrderedDict):
    
    def __getattr__(self, key):
        if key in self:
            return self[key]
        return super(YamlDictionary, self).__getattribute__(key)

    def __setitem__(self, key, value, PREV=0, NEXT=1,
                    dict_setitem=dict.__setitem__):
        super(YamlDictionary, self).__setitem__(key, convert(value), PREV,
                                                NEXT, dict_setitem)
    
    def update(self, other=(), **kwds):
        if isinstance(other, Mapping):
            it = ((k, other[k]) for k in other)
        elif hasattr(other, 'keys'):
            it = ((k, other[k]) for k in other.keys())
        else:
            it = other
        for k, v in it:
            if k in self and isinstance(self[k], Mapping) and\
                             isinstance(v, Mapping):
                self[k].update(v)
            elif k in self and (isinstance(self[k], dict) or
                                isinstance(v, dict)):
                raise ValueError('Can not alter tree topology')
            else:
                self[k] = v
    
    def resolve(self, lookup=None):
        lookup = self if lookup is None else lookup
        for k, v in self.iteritems():
            if isinstance(v, basestring):
                self[k] = v.format(**lookup)
            elif isinstance(v, (YamlDictionary, YamlList)):
                v.resolve(lookup)

class YamlList(list):
    ROOT_NAME = 'root'

    def __init__(self, values=[]):
        super(YamlList, self).__init__(convert(value) for value in values)
    
    def __setitem__(self, key, value):
        super(YamlList, self).__setitem__(key, convert(value))

    def append(self, value):
        super(YamlList, self).append(convert(value))
    
    def resolve(self, lookup=None):
        lookup = {YamlList.ROOT_NAME: self} if lookup is None else lookup
        for i, v in enumerate(self):
            if isinstance(v, basestring):
                self[i] = v.format(**lookup)
            elif isinstance(v, (YamlDictionary, YamlList)):
                v.resolve(lookup)

def convert(value):
    if isinstance(value, dict) and not isinstance(value, YamlDictionary):
        value = YamlDictionary(value)
    elif isinstance(value, list) and not isinstance(value, YamlList):
        value = YamlList(value)
    return value

def load(infile, lookup={}):
    data = yaml.load(infile)
    data.update(lookup)
    data.resolve()
    return data

def constructNode(loader, node):
    if isinstance(node, yaml.MappingNode):
        return constructDictionary(loader, node)
    elif isinstance(node, yaml.SequenceNode):
        return [constructNode(loader, v) for v in node.value]
    return loader.construct_scalar(node)

def constructDictionary(loader, node):
    res = YamlDictionary()
    for k, v in node.value:
        res[k.value] = constructNode(loader, v)
    return res

yaml.add_constructor(u'!yaml_config', constructDictionary)
