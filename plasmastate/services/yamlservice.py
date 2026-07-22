import yaml
from pathlib import Path


class YamlService:
    @staticmethod
    def load_config(config_file):
        try:
            with open(config_file, "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"✗ Configuration file not found: {config_file}")
            return dict()
        except yaml.YAMLError as e:
            print(f"✗ Error parsing YAML: {e}")
            return dict()

    @staticmethod
    def save(path: Path, data: dict):
        with open(path, "w") as outfile:
            yaml.dump(data, outfile, default_flow_style=False)

    @staticmethod
    def dump(dictonary):
        return yaml.dump(dictonary, sort_keys=False)
