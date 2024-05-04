import os
import re
import argparse
import stat
import hashlib

from compiler.devinci_rc.rc_logger import setup_logger
from compiler.devinci_rc.rc_helper import FileParser, FileWriter
from compiler.devinci_rc.utilities import Utilities


# noinspection PyInterpreter
class AliasGenerator:


    def __init__(self, debug=True,logger=None):
        self.debug = debug
        self.bash_function=None
        self.command=None
        self.alias=None
        self.parser=FileParser()
        self.logger=logger if logger else setup_logger(debug=debug)


    def compile_aliases(self, input_file, output_file):
        """
        Compile alias definitions from an .ini file and generate a single aliases.sh file.

        Args:
            input_file (str): Path to the input alias.ini file.
            output_file (str): Path to the output aliases.sh file.

        Returns:
            None
        """
        try:
            pre_path = os.path.join(os.getcwd(), 'docs', 'docstring', 'alias.txt')
            preface = open(pre_path, 'r').read() if os.path.exists(pre_path) else ""

            if self.debug:
                print("Reading alias definitions from the .ini file.")
            # Read alias definitions from the .ini file
            config = self.parser.parse_input_file(input_file)

            if self.debug:
                print("Generating alias commands.")
            # Generate alias commands and write them to the output file
            alias_commands = self.generate_alias_coåmmands(config)
            print(alias_commands)

            writer = FileWriter()
            writer.write_to_file(output_file, f"{preface}\n{alias_commands}")

            if self.debug:
                print("Aliases compilation completed successfully.")

        except Exception as e:
            print(f"An exception occurred: {e}")

    def _find_pattern_in_command(self, command):
        self.logger.info(f"Finding pattern in command: {command}")
        self.logger.debug(f"Executing _find_pattern_in_command with command: {command}")

        command_parts = command.split(' ')
        pattern_matches = [part for part in command_parts if any(
            re.search(pattern, part) for pattern in [r'\$\d', r'<[a-zA-Z]+>'])]
        self.logger.info(f'{len(pattern_matches)} found in command: {command}')
        self.logger.debug(f'{command}\n{pattern_matches},\n{type(pattern_matches)}')
        return pattern_matches

    def generate_alias_commands(self, config):
        alias_commands = []
        for alias_name in config.sections():
            alias = config[alias_name].get('alias', '')
            self.logger.info(f'\n {alias}: {alias_name}')

            alias_commands.append(alias)
            command = config[alias_name].get('command', '')
            script = config[alias_name].get('script', '')

            alias_name = self.normalize_alias(alias_name)

            # Check if the command contains positional arguments
            pattern_matches = self._find_pattern_in_command(command)

            if pattern_matches:
                bash_function_script = self.generate_bash_function(alias,command)
                alias_commands.append(bash_function_script)

                # Set command attribute to reference the path of the created .sh script
                command_attribute = f". {os.path.join('aliases.d', f'{alias}.sh')}"
            else:
                # For aliases without positional arguments, append alias line directly
                alias_line = f"alias \"{alias}\"={config[alias_name].get('main_command', '')} {config[alias_name].get('command', '')}\n"
                alias_commands.append(alias_line)

                # Check if the function name is defined in alias_script to set the alias
                if script and os.path.exists(os.path.join('aliases.d', script)):
                    alias_function_name = alias
                    alias_commands.append(
                        f"alias \"{alias}\"={alias_function_name}\n")
                    self.logger.info(
                        f"Alias function {alias_function_name} created for {alias}")

        return alias_commands

    def generate_bash_function(self, alias, command):
        """
        Generate a bash function script based on the provided alias and command.

        Args:
            alias (str): The alias for the function.
            command (str): The command associated with the alias.

        Returns:
            str: The content of the generated bash function script.
        """
        # Read the content of the stub file
        stub_path = os.path.join('stubs.d', 'alias_function.stub')
        with open(stub_path, 'r') as stub_file:
            stub_content = stub_file.read()

        # Format the stub content with actual values
        bash_function_script = stub_content.format(function_name=alias,command=command, attr="")

        return bash_function_script

    def write_script_to_file(self, script_content, alias):
        """
        Write the provided script content to a .sh file in the aliases.d directory.

        Args:
            script_content (str): The content of the script to be written.
            alias (str): The alias used to generate the script name.

        Returns:
            str: The path to the created script file.
        """
        # Generate a unique script name by appending first 6 characters of SHA-256 hash of alias name
        script_hash = hashlib.sha256(alias.encode()).hexdigest()[:6]
        script_name = f'{alias}_hash{script_hash}.sh'

        # Write the bash function script to a .sh file in the aliases.d directory
        script_file_path = os.path.join('aliases.d', script_name)
        with open(script_file_path, 'w') as script_file:
            script_file.write(script_content)

        # Set the permissions of the .sh file to 711
        os.chmod(script_file_path, stat.S_IRWXU | stat.S_IXGRP | stat.S_IXOTH)

        return script_file_path

    def normalize_alias(self, alias):
        # Replace spaces and hyphens with underscores
        normalized_alias = re.sub(r'[\s-]', '_', alias)
        # Convert camelCase/PascalCase to snake_case
        normalized_alias = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', normalized_alias)
        normalized_alias = re.sub(r'([a-z])([A-Z0-9])', r'\1_\2', normalized_alias)
        # Convert to lowercase
        normalized_alias = normalized_alias.lower()
        return normalized_alias

def main(args):
    if args.input and args.output:
        debug = args.debug if args.debug else False
        alias_generator = AliasGenerator(debug=debug,logger=setup_logger(
            debug=debug)  )
        alias_generator.compile_aliases(args.input, args.output)
    else:
        print("Both input and output files are required.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile alias definitions from an .ini file and generate a single aliases.sh file.")
    parser.add_argument("--input",'-i', help=("Path to the input alias.ini "
                                               "file"))
    parser.add_argument("--output", help="Path to the output aliases.sh file")
    parser.add_argument("--debug", help="Enable debug mode", action="store_true")
    args = parser.parse_args()
    print(args.input, args.output, args.debug)
    main(args)
