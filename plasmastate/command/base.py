from abc import ABC, abstractmethod

from ..core.context import Context


class Command(ABC):
    def __init__(self, context: Context):
        self.context = context

    @abstractmethod
    def run(self) -> int:
        """
        Execute command.

        Returns:
            int: exit code
        """
        pass
