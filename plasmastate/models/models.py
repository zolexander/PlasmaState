from dataclasses import dataclass


@dataclass
class Manifest:
    version: int = 1
    distribution: str | None = None
    plasma_version: str | None = None
