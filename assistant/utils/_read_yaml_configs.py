import yaml
from box import ConfigBox


def read_yaml_configs(path: str) -> ConfigBox:
    """Loads YAML configs """
    with open(path, 'r') as stream:
        cfgs = yaml.safe_load(stream)

    cfgs = ConfigBox(cfgs)

    return cfgs