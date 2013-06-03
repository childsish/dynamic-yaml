import yaml

from _abcoll import Mapping
from collections import OrderedDict

class YamlDictionary(OrderedDict):
    
    def __getattr__(self, key):
        if key in self:
            return self[key]
        return super(YamlDictionary, self).__getattribute__(key)

    def update(self, other=(), **kwds):
        if isinstance(other, Mapping):
            it = ((k, other[k]) for k in other)
        elif hasattr(other, 'keys'):
            it = ((k, other[k]) for k in other.keys())
        else:
            it = other
        for k, v in it:
            if k not in self:
                raise ValueError('Can not alter tree topology')
            elif isinstance(self[k], Mapping) and isinstance(v, Mapping):
                self[k].update(v)
            elif isinstance(self[k], dict) or isinstance(v, dict):
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

    def resolve(self, lookup=None):
        lookup = {YamlList.ROOT_NAME: self} if lookup is None else lookup
        for i, v in enumerate(self):
            if isinstance(v, basestring):
                self[i] = v.format(**lookup)
            elif isinstance(v, (YamlDictionary, YamlList)):
                v.resolve(lookup)

def load(infile, lookup={}):
    infile.seek(0)
    data = yaml.load(infile)
    data.update(lookup)
    data.resolve()
    return data

def construct_sequence(loader, node):
    return YamlList(loader.construct_object(child) for child in node.value)

def construct_mapping(loader, node):
    mapping = YamlDictionary()
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        value = loader.construct_object(value_node)
        mapping[key] = value
    return mapping

yaml.add_constructor(u'tag:yaml.org,2002:seq', construct_sequence)
yaml.add_constructor(u'tag:yaml.org,2002:map', construct_mapping)
