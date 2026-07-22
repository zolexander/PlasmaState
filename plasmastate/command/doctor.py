from .base import Command
from ..providers.factory import ProviderFactory


class DoctorCommand(Command):
    def run(self) -> int:
        """Execute the doctor command."""
        print("PlasmaState Doctor")
        print("------------------")
        print(f"Repository: {self.context.repository}")
        """  
          returns:
            int: exit code
        """
        #providers = ProviderFactory.create(self.context)
        #for provider in providers:
        #    print(provider.collect())
        ProviderFactory.produce_summary(self.context)
        return 0
