import yaml

from .yaml_wrappers import YamlDict, YamlList


def load(infile):
    yaml.FullLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_SEQUENCE_TAG, construct_sequence)
    yaml.FullLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
    data = yaml.load(infile, Loader=yaml.FullLoader)
    data.set_as_root()
    return data


def construct_sequence(loader, node):
    return YamlList(loader.construct_object(child) for child in node.value)


def construct_mapping(loader, node):
    make_obj = loader.construct_object
    return YamlDict((make_obj(k), make_obj(v)) for k, v in node.value)
