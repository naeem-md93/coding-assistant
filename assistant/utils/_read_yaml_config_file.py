import yaml
from box import ConfigBox


def read_yaml_config_file(file_path: str) -> ConfigBox:
    """Loads YAML configs """
    with open(file_path, 'r') as stream:
        cfgs = yaml.safe_load(stream)

    cfgs = ConfigBox(cfgs)

    return cfgs