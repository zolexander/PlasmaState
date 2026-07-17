from .base import Command


class BackupCommand(Command):
    def run(self) -> int:
        """
        Execute the backup command.
        """
        print("PlasmaState Backup")
        print("------------------")
        # Code to create a backup goes here
        print("Backup created successfully.")
        return 0
