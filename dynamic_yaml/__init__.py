import yaml

from yaml_wrappers import YamlDict, YamlList


def load(infile):
    yaml.add_constructor(u'tag:yaml.org,2002:seq', construct_sequence)
    yaml.add_constructor(u'tag:yaml.org,2002:map', construct_mapping)

    data = yaml.load(infile)
    data.set_as_root()
    return data


def construct_sequence(loader, node):
    return YamlList(loader.construct_object(child) for child in node.value)


def construct_mapping(loader, node):
    make_obj = loader.construct_object
    return YamlDict((make_obj(k), make_obj(v)) for k, v in node.value)
