import datetime
import socket
import shutil
import sys
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional

from .base import Provider
from ..services.process import ProcessService
from ..services.yamlservice import YamlService


class ApperanceProvider(Provider):
    def __init__(self, context):
        # Korrekter Aufruf des Basis-Konstruktors in Python
        super().__init__(context)

        # Tools suchen und Pfade als Instanzvariablen speichern
        self.kreadconfig6 = self.find_tool("kreadconfig6", "kreadconfig5")
        self.kwriteconfig6 = self.find_tool("kwriteconfig6", "kwriteconfig5")

        # Große Konfigurations-YAML laden
        self.theme_config = YamlService.load_config(
            "/home/zolexander/PlasmaState/plasmastate/configuration/backup.yaml")
        # theme_keys liegt innerhalb der großen YAML unter providers -> plasma -> theme_keys
                 
    

    @property
    def name(self) -> str:
        return "apperance"

    def collect(self):
        data: dict = {
            "meta": {
                "created": datetime.datetime.now().isoformat(timespec="seconds"),
                "host": socket.gethostname(),
            },
            "settings": {},
        }

        # theme_keys liegt innerhalb der großen YAML unter providers -> plasma -> theme_keys
        providers = self.theme_config.get("providers", {})
        plasma_cfg = providers.get("plasma", {})
        theme_keys = plasma_cfg.get("theme_keys", {})

        # Dynamisch durch die Kategorien und deren Items iterieren
        for category, items in theme_keys.items():
            data["settings"][category] = {}

            for item in items:
                label = item["label"]
                file_name = item["file"]
                group = item["group"]
                key = item["key"]

                # Wert über kread auslesen statt IniService
                value = self.kread(file_name, group, key)

                # kreadconfig gibt oft einen leeren String zurück, wenn der Key fehlt
                if value and value.strip():
                    data["settings"][category][label] = value.strip()

            # Lokales Farbschema mitsichern, falls vorhanden
        colors_settings = data["settings"].get("colors", {})
        color_scheme_name = colors_settings.get("ColorScheme", "")

        color_file = self.find_color_scheme_file(color_scheme_name)
        if color_file and color_file.is_relative_to(Path.home()):
            data["colors_file_content"] = color_file.read_text()
            data["colors_file_name"] = color_file.name
        return data

    def backup(self, out_path: Path) -> None:
        data: dict = {
            "meta": {
                "created": datetime.datetime.now().isoformat(timespec="seconds"),
                "host": socket.gethostname(),
            },
            "settings": {},
        }

        # theme_keys liegt innerhalb der großen YAML unter providers -> plasma -> theme_keys
        providers = self.theme_config.get("providers", {})
        plasma_cfg = providers.get("plasma", {})
        theme_keys = plasma_cfg.get("theme_keys", {})

        # Dynamisch durch die Kategorien und deren Items iterieren
        for category, items in theme_keys.items():
            data["settings"][category] = {}

            for item in items:
                label = item["label"]
                file_name = item["file"]
                group = item["group"]
                key = item["key"]

                # Wert über kread auslesen statt IniService
                value = self.kread(file_name, group, key)

                # kreadconfig gibt oft einen leeren String zurück, wenn der Key fehlt
                if value and value.strip():
                    data["settings"][category][label] = value.strip()

        # Lokales Farbschema mitsichern, falls vorhanden
        colors_settings = data["settings"].get("colors", {})
        color_scheme_name = colors_settings.get("ColorScheme", "")

        color_file = self.find_color_scheme_file(color_scheme_name)
        if color_file and color_file.is_relative_to(Path.home()):
            data["colors_file_content"] = color_file.read_text()
            data["colors_file_name"] = color_file.name

        # Backup-Datei schreiben (out_path wurde als Parameter übergeben)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=100)
        )
        print(f"Theme-Backup gespeichert: {out_path}")

    def backup_file(self, path: Path):
        if path.exists():
            ts = datetime.datetime.now().strftime("%Y%m&d-%H%M%S")
            shutil.copy2(path, path.with_suffix(path.suffix + f".back-{ts}"))

    def restore(self, data: dict) -> None:
        print("Restoring Plasma Information not supported yet")

    def validate(self) -> List[str]:
        print("validate not supported yet")
        messages = ["str"]
        return messages

    # Da find_tool in __init__ aufgerufen wird, muss es als statische Methode
    # oder normale Funktion ohne 'self' (oder als @classmethod) definiert sein.

    def find_tool(self, name6: str, name5: str) -> str:
        path = shutil.which(name6) or shutil.which(name5)
        if not path:
            sys.exit(
                f"Weder {name6} noch {name5} wurde gefunden.\n"
                f"Installiere sie zum Beispiel mit: apt install libkf6config-bin\n"
            )
        return path

    def kread(self, file: str, group: str, key: str) -> str:
        # Führt das gefundene kreadconfig-Tool aus
        return ProcessService.run(
            [self.kreadconfig6, "--file", file, "--group", group, "--key", key]
        )

    # Fehlendes Komma bei den Parametern korrigiert und --key korrigiert (Zuweisung von 'value')
    def kwrite(self, file: str, group: str, key: str, value: str):
        return ProcessService.run(
            [self.kwriteconfig6, "--file", file, "--group", group, "--key", key, value]
        )

    def find_color_scheme_file(self, name: str) -> Optional[Path]:
        if not name:
            return None

        # Suchpfade aus der großen YAML holen: providers -> plasma -> color_scheme_dir
        providers = self.theme_config.get("providers", {})
        plasma_cfg = providers.get("plasma", {})
        search_dirs = plasma_cfg.get("color_scheme_dir", [])

        for d in search_dirs:
            # Bereinigt potenzielle Kommas aus der YAML und löst Pfade auf (~/)
            d_clean = d.rstrip(",").strip()

            if d_clean.startswith("~"):
                base_path = Path(d_clean).expanduser()
            elif d_clean.startswith("/"):
                base_path = Path(d_clean)
            else:
                base_path = Path.home() / d_clean

            p = base_path / f"{name}.colors"
            if p.exists():
                return p
        return None
