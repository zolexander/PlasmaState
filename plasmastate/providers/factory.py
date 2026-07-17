from ..core.context import Context
from .system import SystemProvider


class ProviderFactory:
    @staticmethod
    def create(context: Context):

        providers = {SystemProvider(context)}
        return providers
