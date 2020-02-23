import yaml


def add_constructors(loader):
    from .yaml_wrappers import YamlDict, YamlList

    def _construct_sequence(loader, node):
        return YamlList(loader.construct_object(child) for child in node.value)

    def _construct_mapping(loader, node):
        return YamlDict((loader.construct_object(k), loader.construct_object(v)) for k, v in node.value)

    loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_SEQUENCE_TAG, _construct_sequence)
    loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


class DynamicYamlLoader(yaml.FullLoader):
    pass


add_constructors(DynamicYamlLoader)


def load(stream, loader=DynamicYamlLoader):
    data = yaml.load(stream, Loader=loader)
    data.set_as_root()
    return data
