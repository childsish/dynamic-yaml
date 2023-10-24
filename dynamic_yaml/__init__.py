import yaml

from typing import Type


class DynamicYamlLoader(yaml.FullLoader):
    def __init__(self, stream):
        super().__init__(stream)
        self.root = None


def add_wrappers(loader: Type[DynamicYamlLoader]):
    from .yaml_wrappers import DynamicYamlObject, YamlDict, YamlList

    def _construct_dynamic_dict(loader_: DynamicYamlLoader, node: yaml.MappingNode) -> YamlDict:
        loader_.flatten_mapping(node)
        return YamlDict(((loader_.construct_object(key), loader_.construct_object(value)) for key, value in node.value))

    def _construct_dynamic_list(loader_: DynamicYamlLoader, node: yaml.SequenceNode) -> YamlList:
        return YamlList((loader_.construct_object(child) for child in node.value))

    def _represent_dynamic_dict(dumper: yaml.BaseDumper, data: YamlDict):
        return dumper.represent_mapping(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, {key: data[key] for key in data._collection})

    def _represent_dynamic_list(dumper: yaml.BaseDumper, data: YamlList):
        return dumper.represent_sequence(yaml.resolver.BaseResolver.DEFAULT_SEQUENCE_TAG, [data[key] for key in range(len(data._collection))])

    loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_dynamic_dict)
    loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_SEQUENCE_TAG, _construct_dynamic_list)
    yaml.add_representer(YamlDict, _represent_dynamic_dict)
    yaml.add_representer(YamlList, _represent_dynamic_list)


def load(stream, loader=DynamicYamlLoader, recursive=False):
    result = yaml.load(stream, Loader=loader)
    result._set_as_root(recursive=recursive)
    return result


def dump(data, *args, **kwargs):
    return yaml.dump(data, *args, **kwargs)


add_wrappers(DynamicYamlLoader)
