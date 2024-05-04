import os
import configparser
import inspect
import shlex
from typing import List, Tuple


class Utilities:
    @staticmethod
    def print_classes(module: object)->None:
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                print(name)

    @staticmethod
    def create_centered_banner(text):
        width = 86
        banner = f"#{text:^{width}}"
        border = f"#{'=' * width}"
        return f"\n{border}\n{banner}\n{border}\n"

    @staticmethod
    def parse_ini_file(ini_file: str = None) -> List[Tuple[str, str, str, str]]:
        """
        Parse the provided .ini file or search for alias.ini upwards in the directory tree
        until registration.d is found, to extract alias information.

        Args:
            ini_file (str, optional): Path to the .ini file containing alias definitions.
                If not provided, search for alias.ini in the directory tree.

        Returns:
            list: A list of tuples containing (alias, command) extracted from the .ini file.
        """
        alias_info_list = []

        # If ini_file is not provided, search for alias.ini in the directory tree
        if ini_file is None:
            current_dir = os.getcwd()
            while current_dir != os.path.abspath('/'):  # Stop at root directory
                ini_file = os.path.join(current_dir, 'alias.ini')
                if os.path.exists(ini_file):
                    break
                current_dir = os.path.dirname(current_dir)
            else:
                raise FileNotFoundError(
                    "alias.ini not found in the directory tree.")

        config = configparser.ConfigParser()
        config.read(ini_file)

        for section in config.sections():
            name = section
            alias = config[section].get('alias', '')
            command = config[section].get('command', '')
            bin = config[section].get('main_command', '')

            if alias and command:
                alias_info_list.append((name, bin, alias, command))

        return alias_info_list

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

    @staticmethod
    def create_md_for_each_mod(path):
        os.chdir(path if os.path.exists(path) else os.getcwd())
        for file in os.listdir():
            if file.endswith('.py' and '__init__' not in file):
                with open(file, 'r') as f:
                    lines = f.readlines()
                with open(file.replace('.py', '.md'), 'w') as f:
                    f.write(f"# {file.replace('.py', '')}\n")
                    for line in lines:
                        if line.startswith('class'):
                            f.write(f"## {line.replace('class', '').replace(':', '').strip()}\n")
                        elif line.startswith('    def'):
                            f.write(f"### {line.replace('def', '').replace(':', '').strip()}\n")
                        elif line.startswith('        '):
                            f.write(f"#### {line.strip()}\n")
                        elif line.startswith('    '):
                            f.write(f"### {line.strip()}\n")
                        else:
                            f.write(f"{line}\n")
                print(f"Created {file.replace('.py', '.md')}")
