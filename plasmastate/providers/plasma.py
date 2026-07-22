import datetime
import socket
import os
from pathlib import Path
from typing import List, Optional

from .base import Provider
from ..services.plasma.parser import AppletSrcParser 
from ..services.plasma.analyzer import PlasmaAnalyzer
from ..services.plasma.plasmavalidator import PlasmaValidator


CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
APPLETS_FILE = CONFIG_DIR / "plasma-org.kde.plasma.desktop-appletsrc"


class PlasmaProvider(Provider):
    def __init__(self, context):
        super().__init__(context)
        self.parser = AppletSrcParser()
        self.analyzer = PlasmaAnalyzer()
        self.validator = PlasmaValidator()


    @property
    def name(self) -> str:
        return "plasma"

    def collect(self) -> dict:
        with open(APPLETS_FILE,"r") as inputfile:
            groups = self.parser.parse(inputfile)
            res=  self.analyzer.full_panel_dump(groups)
            return res

    def restore(self, data: dict) -> None:
        print("Plasma restore not implemented in provider; use dedicated tooling.")

    def validate(self) -> List[str]:
        msgs: List[str] = []
        if not APPLETS_FILE.exists():
            msgs.append(f"appletrc file not found: {APPLETS_FILE}")
            return msgs
        try:
            _ = APPLETS_FILE.read_text()
        except Exception as e:
            msgs.append(f"Cannot read {APPLETS_FILE}: {e}")
        return msgs
