from .doctor import DoctorCommand
from .backup import BackupCommand
from .restore import RestoreCommand
from .validate import ValidateCommand


class CommandFactory:
    def create(name, context):

        match name:
            case "doctor":
                return DoctorCommand(context)

            case "backup":
                return BackupCommand(context)
            case "restore":
                return RestoreCommand(context)
            case "validate":
                return ValidateCommand(context)
