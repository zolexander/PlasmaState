from ..core.context import Context
from .system import SystemProvider
from .plasma import PlasmaProvider
from .apperance import ApperanceProvider
from .apt import AptProvider
# Importiere hier auch deine anderen Provider, sobald du sie hast:
# from .apt import AptProvider
# from .kwin import KwinProvider
# from .plasmoid import PlasmoidProvider

from ..services.yamlservice import YamlService
from pathlib import Path
import datetime
import socket
from typing import Iterable


class ProviderFactory:
    # Hier mappen wir die YAML-Schlüssel direkt auf die Klassen
    _PROVIDER_MAP = {
        "system": SystemProvider,
        "plasma": PlasmaProvider,
        "apperance": ApperanceProvider,
        "apt": AptProvider
        # "apt": AptProvider,
        # "kwin": KwinProvider,
        # "plasmoid": PlasmoidProvider,
    }

    @staticmethod
    def create(context: Context) -> set:
        config = YamlService.load_config(
            Path.cwd() / "plasmastate/configuration/backup.yaml"
        )

        active_providers = set()
        provider_configs = config.get("providers", {})

        for key, provider_class in ProviderFactory._PROVIDER_MAP.items():
            # Holt die Config für den jeweiligen Provider (z.B. {"enabled": True})
            # Falls er in der YAML fehlt, wird standardmäßig False angenommen
            cfg = provider_configs.get(key, {})

            if cfg.get("enabled", False):
                # Hier wird der Provider dynamisch instanziiert und dem Set hinzugefügt
                active_providers.add(provider_class(context))
        return active_providers

    @staticmethod
    def produce_summary(context: Context, out_path: Path | None = None) -> Path:
        """Instantiates enabled providers, collects their data and writes a
        combined YAML summary to `out_path` (or `providers-collect-summary.yaml`).
        Returns the path written to.
        """
        providers = ProviderFactory.create(context)
        summary = {
            "meta": {
                "created": datetime.datetime.now().isoformat(timespec="seconds"),
                "host": socket.gethostname(),
            },
            "providers": {},
            "errors": {},
        }

        for p in sorted(list(providers), key=lambda x: x.name):
            try:
                data = p.collect()
                summary["providers"][p.name] = data
            except Exception as e:
                summary["errors"][p.name] = str(e)

        out = out_path or (Path.cwd() / "providers-collect-summary.yaml")
        YamlService.save(out, summary)
        print(f"Collected information is saved at the {out} Path")
        return out
