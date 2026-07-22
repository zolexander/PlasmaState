from .base import Provider


class SystemProvider(Provider):
    @property
    def name(self) -> str:
        return "system"

    def collect(self) -> dict:
        """
        Collect system information and return it as a dictionary.
        """
        import platform
        import os
        import psutil

        system_info = {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "platform_release": platform.release(),
            "architecture": platform.architecture(),
            
        }
        return system_info

    def restore(self, data: dict) -> None:
        """
        Restore system information from the provided data.
        Note: Restoring system information is not typically feasible or safe.
        This method will log the data instead of attempting to restore it.
        """
        print("Restoring system information is not supported.")
        print("Received data:", data)

    def validate(self) -> list[str]:
        """
        Validate the system's configuration and connectivity.
        Returns a list of validation messages.
        """
        import platform
        import psutil

        messages = []

        # Validate platform
        if platform.system() not in ["Linux", "Windows", "Darwin"]:
            messages.append(f"Unsupported platform: {platform.system()}")

        # Validate CPU count
        cpu_count = psutil.cpu_count(logical=True)
        if cpu_count is None:
            messages.append("No CPUs detected.")

        # Validate memory
        memory_total = psutil.virtual_memory().total
        if memory_total < 512 * 1024 * 1024:  # Less than 512MB
            messages.append("Insufficient memory detected.")

        return messages
