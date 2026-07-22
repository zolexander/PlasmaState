from configparser import ConfigParser
from pathlib import Path
from typing import Optional


class IniService:
    # Hier speichern wir den geladenen Parser intern
    _parser: Optional[ConfigParser] = None
    _default_path: Path = Path.home() / ".config" / "kdeglobals"

    @classmethod
    def read(cls, path: Path) -> ConfigParser:
        """Lädt die Datei explizit und speichert sie im Cache."""
        cls._parser = ConfigParser(interpolation=None)
        cls._parser.read(path)
        return cls._parser

    @classmethod
    def get(cls, section: str, key: str, path: Optional[Path] = None) -> Optional[str]:
        """Holt einen Wert. Lädt die Datei automatisch, falls noch nicht geschehen."""
        if cls._parser is None:
            # Falls noch nicht gelesen wurde, nutzen wir den übergebenen oder den Standardpfad
            return None

        # Sicherstellen, dass die Section und der Key existieren, um Fehler zu vermeiden
        if cls._parser.has_option(section, key) is not None:
            return cls._parser.get(section, key)
        return None
