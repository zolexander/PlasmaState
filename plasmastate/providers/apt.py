from .base import Provider
from  ..services.packetManager.apt import AptManager
from pathlib import Path
from ..services.yamlservice import YamlService
import fnmatch
import re
def is_ignored(item: str, pattern: str) -> bool:
    if pattern.endswith("*"):
        # Schneidet das '*' ab und prüft, ob der String damit anfängt
        prefix = pattern[:-1]
        return item.startswith(prefix)
    return item == pattern


def filter_ignored(data_list: list[str], ignored_items: list[str]) -> list[str]:
    return [
        item
        for item in data_list
        if not any(is_ignored(item, pattern) for pattern in ignored_items)
    ]
class AptProvider(Provider):
    

    @property
    def name(self) ->str:
        return "apt"
    
    def collect(self)-> dict:
        manager = AptManager()
        config = YamlService.load_config(
            Path.cwd() / "plasmastate/configuration/backup.yaml"
        )
        provider_config = config.get("providers")
        apt_config = provider_config.get("apt")
        ignore = apt_config.get("ignore")
        all_packages = manager.showmanual().splitlines()
        packages = filter_ignored(all_packages,ignore)
        return sorted(packages)
        
    def restore(self, data):
        return NotImplementedError
    def backup(self):
        return NotImplementedError
    def validate(self):
        return NotImplementedError