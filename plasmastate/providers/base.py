from abc import ABC, abstractmethod

from ..core.context import Context


class Provider(ABC):
    def __init__(self, context: Context):
        self.context = context

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Unique name of the provider.
        """
        ...

    @abstractmethod
    def collect(self) -> dict:
        """collect the data from the provider and return it as a dictionary."""
        ...

    @abstractmethod
    def restore(self, data: dict) -> None:
        """
        Restore the data from the provider.
        """
        ...

    @abstractmethod
    def validate(self) -> list[str]:
        """
        Validate the provider's configuration and connectivity.
        """
        ...
