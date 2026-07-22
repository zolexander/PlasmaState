from dataclasses import dataclass, field
from typing import Any

from .plasmaconstants import PanelLocation, PanelFormFactor


@dataclass
class Applet:
    id: int
    plugin: str
    configuration: dict[str, Any] = field(default_factory=dict)
    contained_applets: list["Applet"] = field(default_factory=list)

    @classmethod
    def from_dict(cls,data):
        return cls(
            id=data["id"],
            plugin=data["plugin"],
            configuration=data["configuration"],
            contained_applets=[
                cls.from_dict(child)
                for child in data.get("contained_applets", [])
            ],
        )

@dataclass
class Containment:
    id: int
    plugin: str
    properties: dict[str, Any] = field(default_factory=dict)
    applets: list[Applet] = field(default_factory=list)
    

@dataclass
class Panel(Containment):

    screen: int | None = None
    location: PanelLocation | None = None
    formfactor: PanelFormFactor | None = None
    @classmethod
    def from_dict(cls, data: dict):

        return cls(
        id=data["id"],
        plugin=data["plugin"],
        properties=data.get("properties", {}),
        applets=[
            Applet.from_dict(applet)
            for applet in data.get("applets", [])
        ],
        screen=data.get("screen"),
        location=data.get("location"),
        formfactor=data.get("formfactor"),
    )