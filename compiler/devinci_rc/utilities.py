import inspect
import shlex


class Utilities:
    @staticmethod
    def print_classes(module):
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                print(name)
    @staticmethod
    def sanitize_command(command):
        if command is None or command == '':
            raise ValueError("Command cannot be None or empty")

        # Strip leading and trailing whitespaces
        command = command.strip()

        # Escape potentially harmful characters or sequences
        command = shlex.quote(command)

        # Validate command against a list of allowed commands
        # allowed_commands = ['ls', 'cd', 'pwd', ...]
        # if command not in allowed_commands:
        #     raise ValueError("Invalid command")

        return command