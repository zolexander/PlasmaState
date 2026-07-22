from pathlib import Path

from .yamlservice import YamlService

CONFIG_PATH = Path(__file__).resolve().parent.parent / "configuration" / "backup.yaml"


def load_search_paths(config_path: Path | None = None) -> list[Path]:
    path = config_path or CONFIG_PATH
    config = YamlService.load_config(path)
    provider_config = config.get("providers", {})
    search_paths = provider_config.get("search_paths", [])

    if not search_paths:
        return []

    return [Path(search_path).expanduser() for search_path in search_paths]


SEARCH_PATHS = load_search_paths()


class ConfigService:
    @staticmethod
    def find(configfile: str) -> Path | None:
        for directory in SEARCH_PATHS:
            path = directory / configfile
            if path.exists():
                return path

        return None

