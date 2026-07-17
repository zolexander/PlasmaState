from .base import Command


class DoctorCommand(Command):
    def run(self) -> int:
        """
                Execute the doctor command.
        :"""
        print("PlasmaState Doctor")
        print("------------------")
        print(f"Repository: {self.context.repository}")
        """  
          returns:
            int: exit code
        """

        return 0
