from __future__ import annotations
import subprocess


class ProcessService:

    @staticmethod
    def run(command: list[str]) -> str:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )

        return result.stdout.strip()