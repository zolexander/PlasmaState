from pathlib import Path


class Context:
    def __init__(self, repository: Path):
        self.repository = repository
        self.manifest = repository / "manifest.yaml"
