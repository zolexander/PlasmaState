from .doctor import DoctorCommand
from .backup import BackupCommand
from .restore import RestoreCommand
from .validate import ValidateCommand
from ..core.context import Context


class CommandFactory:
    @staticmethod
    def create(command: str, context: Context):

        commands = {
            "backup": BackupCommand,
            "restore": RestoreCommand,
            "doctor": DoctorCommand,
            "validate": ValidateCommand,
        }

        command_class = commands.get(command)

        if command_class is None:
            raise ValueError(f"Unknown command: {command}")

        return command_class(context)
